package binanceservice

import (
	"algo_api/internal/utils"
	"context"
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
		instance = NewService()
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

func NewService() IService {
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
	GetChartData(symbol string, start int, end int, timeframe string) ([]Candlestick, error)
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

func (s *BinanceService) GetChartData(symbol string, start int, end int, timeframe string) ([]Candlestick, error) {
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
