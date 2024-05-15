package binanceservice

import (
	"algo_api/internal/utils"
	"context"
	"errors"
	"fmt"
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
	GetAmount(symbol string) (string, error)
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

func (s *BinanceService) GetAmount(symbol string) (string, error) {
	response, err := s.client.NewGetAccountService().Do(context.Background())
	if err != nil {
		logrus.WithFields(logrus.Fields{
			"err": err,
		}).Error("Could not get coin balances")
		return "0.0", nil
	}
	amount := 0.0
	for _, balance := range response.Balances {
		if balance.Asset == symbol {
			amount = utils.String2float(balance.Free) + utils.String2float(balance.Locked)
			break
		}
	}
	return utils.Float2String(amount), nil
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
		amount := utils.String2float(balance.Free) + utils.String2float(balance.Locked)
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
		balanceTotal += amount * utils.String2float(price)
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

func (s *BinanceService) getMinMaxOrderQuantity(symbol string) (string, string, error) {
	exchangeInfo, err := s.client.NewExchangeInfoService().Do(context.Background())
	if err != nil {
		return "", "", err
	}

	for _, s := range exchangeInfo.Symbols {
		if s.Symbol == (symbol + "USDT") {
			for _, filter := range s.Filters {
				if filter.FilterType == "LOT_SIZE" {
					return filter.MinQty, filter.MaxQty, nil
				}
			}
		}
	}

	return "", "", errors.New("could not find symbol")
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

func (s *BinanceService) Buy(symbol string) error {
	usdt, err := s.GetAmount("USDT")
	if err != nil {
		logrus.Error("Could not get USDT amount")
		return err
	}

	btcPrice, err := s.GetPrice(symbol)
	if err != nil {
		logrus.WithFields(logrus.Fields{
			"symbol": symbol,
		}).Error("Could not get price")
		return err
	}

	amount := utils.String2float(btcPrice) / utils.String2float(usdt)

	// "<APIError> code=-1013, msg=Filter failure: LOT_SIZE
	_, maxOrderQuantity, err := s.getMinMaxOrderQuantity(symbol)
	if err != nil {
		logrus.Error(err)
		return err
	}

	// fix: <APIError> code=-1111, msg=Parameter 'quantity' has too much precision.
	precision, err := s.getOrderPrecision(symbol)
	if err != nil {
		logrus.Error(err)
		return err
	}

	logrus.WithFields(logrus.Fields{
		"amount":             amount,
		"precision":          precision,
		"max order quantity": maxOrderQuantity,
	}).Info("Buy: started")

	amountCompleted := 0.0
	for amountCompleted < amount {
		chunk := utils.String2float(maxOrderQuantity) / utils.String2float(btcPrice)

		chunk2 := utils.String2float(fmt.Sprintf("%.8f", chunk))

		logrus.WithFields(logrus.Fields{
			"chunk": chunk2,
		}).Info("Buy: chunk")

		_, err = s.client.NewCreateOrderService().
			Symbol(symbol + "USDT").
			Side("BUY").
			Type("MARKET").
			Quantity(chunk2).
			Do(context.Background())

		if err != nil {
			amountCompleted = amountCompleted + chunk2
		}

		if err != nil {
			logrus.Error(err)
			return err
		}
	}

	return err
}

func (s *BinanceService) Sell(symbol string) error {
	_, err := s.client.NewCreateOrderService().
		Symbol(symbol + "USDT").
		Side("SELL").
		Type("MARKET").
		Quantity(0.5).
		Do(context.Background())
	return err
}
