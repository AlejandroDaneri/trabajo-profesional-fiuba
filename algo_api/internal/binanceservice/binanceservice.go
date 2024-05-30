package binanceservice

import (
	"algo_api/internal/utils"
	"context"
	"errors"
	"fmt"
	"math"
	"os"
	"sync"

	binance_connector "github.com/binance/binance-connector-go"
	"github.com/sirupsen/logrus"
)

var instance IService
var once sync.Once

func GetInstance() IService {
	once.Do(func() {
		instance = NewServiceUsingEnvVars()
	})
	return instance
}

type Candlestick struct {
	OpenTime  uint64 `json:"open_time"`
	CloseTime uint64 `json:"close_time"`
	Open      string `json:"open"`
	Close     string `json:"close"`
}

type BinanceService struct {
	client *binance_connector.Client
}

func NewService(APIKey string, APISecret string) IService {
	baseURL := "https://testnet.binance.vision"

	client := binance_connector.NewClient(APIKey, APISecret, baseURL)
	return &BinanceService{
		client: client,
	}
}

func NewServiceUsingEnvVars() IService {
	apiKey := os.Getenv("EXCHANGE_BINANCE_API_KEY")
	secretKey := os.Getenv("EXCHANGE_BINANCE_API_SECRET")
	baseURL := "https://testnet.binance.vision"

	client := binance_connector.NewClient(apiKey, secretKey, baseURL)
	return &BinanceService{
		client: client,
	}
}

type IService interface {
	GetPrice(symbol string) (string, error)
	GetBalance() (string, error)
	GetAmount(symbol string) (float64, error)
	GetCandleticks(symbol string, start int, end int, timeframe string) ([]Candlestick, error)
	Buy(symbol string) error
	Sell(symbol string) error
}

func (s *BinanceService) GetPrice(symbol string) (string, error) {
	ticker, err := s.client.NewTickerService().Symbol(symbol + "USDT").Do(context.Background())
	if err != nil {
		logrus.WithFields(logrus.Fields{
			"err":    err,
			"symbol": symbol,
		}).Error("Could not get price")
		return "", err
	}
	return ticker.LastPrice, nil
}

func (s *BinanceService) GetAmount(symbol string) (float64, error) {
	response, err := s.client.NewGetAccountService().Do(context.Background())
	if err != nil {
		logrus.WithFields(logrus.Fields{
			"err": err,
		}).Error("Could not get coin balances")
		return 0, nil
	}
	amount := 0.0
	for _, balance := range response.Balances {
		if balance.Asset == symbol {
			amount = utils.String2Float(balance.Free) + utils.String2Float(balance.Locked)
			break
		}
	}
	return amount, nil
}

func (s *BinanceService) GetBalance() (string, error) {
	response, err := s.client.NewGetAccountService().Do(context.Background())
	if err != nil {
		logrus.WithFields(logrus.Fields{
			"err": err,
		}).Error("Could not get coin balances")
		return "0", nil
	}
	balanceTotal := 0.0
	for _, balance := range response.Balances {
		symbol := balance.Asset
		amount := utils.String2Float(balance.Free) + utils.String2Float(balance.Locked)
		if symbol == "USDT" {
			balanceTotal += amount
		}
		// only we are using balances for this currencies
		if symbol != "BTC" && symbol != "ETH" && symbol != "SOL" {
			continue
		}
		price, err := s.GetPrice(symbol)
		if err != nil {
			continue
		}
		balanceTotal += amount * utils.String2Float(price)
	}

	return fmt.Sprintf("%.2f", balanceTotal), nil
}

func (s *BinanceService) GetCandleticks(symbol string, start int, end int, timeframe string) ([]Candlestick, error) {
	response, err :=
		s.client.
			NewUIKlinesService().
			Symbol(symbol + "USDT").
			Interval(timeframe).
			StartTime(uint64(start * 1000)).
			EndTime(uint64(end * 1000)).
			Do(context.Background())
	if err != nil {
		return []Candlestick{}, err
	}
	candlesticks := []Candlestick{}
	for _, kline := range response {
		candlesticks = append(candlesticks, Candlestick{
			OpenTime:  kline.OpenTime / 1000,
			CloseTime: kline.CloseTime / 1000,
			Open:      kline.Open,
			Close:     kline.Close,
		})
	}
	return candlesticks, nil
}

// https://github.com/binance/binance-spot-api-docs/blob/master/filters.md#min_notional
func (s *BinanceService) getMinNotional(symbol string) (float64, error) {
	exchangeInfo, err := s.client.NewExchangeInfoService().Do(context.Background())
	if err != nil {
		return 0, err
	}

	for _, s := range exchangeInfo.Symbols {
		if s.Symbol == (symbol + "USDT") {
			for _, filter := range s.Filters {
				if filter.FilterType == "NOTIONAL" {
					return utils.String2Float(filter.MinNotional), nil
				}
			}
		}
	}

	return 0, errors.New("min notional not found")
}

// https://github.com/binance/binance-spot-api-docs/blob/master/filters.md#lot_size
func (s *BinanceService) getOrderInfo(symbol string) (minQty, maxQty, stepSize float64, err error) {
	exchangeInfo, err := s.client.NewExchangeInfoService().Do(context.Background())
	if err != nil {
		return 0, 0, 0, err
	}

	for _, s := range exchangeInfo.Symbols {
		if s.Symbol == (symbol + "USDT") {
			for _, filter := range s.Filters {
				if filter.FilterType == "LOT_SIZE" {
					return utils.String2Float(filter.MinQty), utils.String2Float(filter.MaxQty), utils.String2Float(filter.StepSize), nil
				}
			}
		}
	}

	return 0, 0, 0, errors.New("could not find symbol")
}

func adjustQuantityForLotSize(quantity, minQty, maxQty, stepSize float64) float64 {
	if quantity < minQty {
		return minQty
	}
	if quantity > maxQty {
		return maxQty
	}
	return math.Floor(quantity/stepSize) * stepSize
}

func (s *BinanceService) getOrderPrecision(symbol string) (int64, error) {
	exchangeInfo, err := s.client.NewExchangeInfoService().Do(context.Background())
	if err != nil {
		return 0, err
	}

	for _, s := range exchangeInfo.Symbols {
		if s.Symbol == (symbol + "USDT") {
			return s.BaseAssetPrecision, nil
		}
	}

	return 0, errors.New("could not find symbol")
}

func (s *BinanceService) processQuantity(initialQuantity, min, max, step float64) float64 {
	// "<APIError> code=-1013, msg=Filter failure: LOT_SIZE
	qty := adjustQuantityForLotSize(initialQuantity, min, max, step)

	// fix: <APIError> code=-1111, msg=Parameter 'quantity' has too much precision.
	// TO-DO: use precision here
	formattedQty := utils.String2Float(fmt.Sprintf("%.8f", qty))

	return formattedQty
}

func (s *BinanceService) Buy(symbol string) error {
	min, max, step, err := s.getOrderInfo(symbol)
	if err != nil {
		logrus.Error(err)
		return err
	}

	minNotional, err := s.getMinNotional(symbol)
	if err != nil {
		return err
	}

	_, err = s.getOrderPrecision(symbol)
	if err != nil {
		logrus.Error(err)
		return err
	}

	logrus.WithFields(logrus.Fields{
		"symbol": symbol,
	}).Info("Buy: started")
	for {
		usdt, err := s.GetAmount("USDT")
		if err != nil {
			continue
		}

		amount, err := s.GetAmount(symbol)
		if err != nil {
			continue
		}

		logrus.WithFields(logrus.Fields{
			"symbol": symbol,
			"usdt":   usdt,
			"amount": amount,
		}).Info("Buy: progress")

		if usdt < minNotional {
			logrus.WithFields(logrus.Fields{
				"symbol": symbol,
			}).Info("Buy: completed")
			break
		}

		_, err = s.client.NewCreateOrderService().
			Symbol(symbol + "USDT").
			Side("BUY").
			Type("MARKET").
			QuoteOrderQty(s.processQuantity(usdt, min, max, step)).
			Do(context.Background())

		if err != nil {
			logrus.Info(err)
		}
	}

	return nil
}

func (s *BinanceService) closeOpenOrders(symbol string) error {
	openOrders, err := s.client.NewCancelOpenOrdersService().Symbol(symbol + "USDT").Do(context.Background())
	if err != nil {
		return err
	}

	for _, order := range openOrders {
		_, err := s.client.NewCancelOrderService().Symbol(symbol + "USDT").OrderId(order.OrderId).Do(context.Background())
		if err != nil {
			continue
		}
	}

	return nil
}

func (s *BinanceService) Sell(symbol string) error {
	logrus.WithFields(logrus.Fields{
		"symbol": symbol,
	}).Info("Sell: started")

	minNotional, err := s.getMinNotional(symbol)
	if err != nil {
		return err
	}

	for {
		s.closeOpenOrders(symbol)

		price, err := s.GetPrice(symbol)
		if err != nil {
			return err
		}

		amount, err := s.GetAmount(symbol)
		if err != nil {
			return err
		}

		usdt, err := s.GetAmount("USDT")
		if err != nil {
			return err
		}

		logrus.WithFields(logrus.Fields{
			"symbol": symbol,
			"usdt":   usdt,
			"amount": amount,
		}).Info("Sell: progress")

		if amount*utils.String2Float(price) < minNotional {
			logrus.WithFields(logrus.Fields{
				"symbol": symbol,
			}).Info("Sell: completed")
			break
		}

		_, err = s.client.NewCreateOrderService().
			Symbol(symbol + "USDT").
			Side("SELL").
			Type("LIMIT").
			Price(utils.String2Float(price)).
			TimeInForce("GTC").
			Quantity(amount).
			Do(context.Background())

		if err != nil {
			logrus.Info(err)
		}
	}
	return nil
}
