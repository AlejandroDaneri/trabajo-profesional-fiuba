package pythonservice

import (
	"encoding/json"
	"io"
	"net/http"
	"net/url"
	"sync"

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

type PythonService struct {
}

func NewService() IService {
	return &PythonService{}
}

type IService interface {
	GetBacktesting(coin string, initial_balance string, start string, end string) (Backtesting, error)
}

type Backtesting struct {
	FinalBalance string `json:"final_balance"`
}

func (s *PythonService) GetBacktesting(coin string, initial_balance string, start string, end string) (Backtesting, error) {
	baseURL := "http://backtester:5000"
	endpoint := "backtest"

	params := url.Values{}
	params.Add("coin", coin)
	params.Add("initial_balance", initial_balance)
	params.Add("data_from", start)
	params.Add("data_to", end)

	url := baseURL + "/" + endpoint + "?" + params.Encode()

	response, err := http.Get(url)
	if err != nil {
		return Backtesting{}, err
	}
	defer response.Body.Close()

	body, err := io.ReadAll(response.Body)
	if err != nil {
		return Backtesting{}, err
	}

	var backtesting Backtesting
	err = json.Unmarshal(body, &backtesting)
	if err != nil {
		logrus.Error("Could not unmarshal")
		return Backtesting{}, err
	}
	return backtesting, nil
}
