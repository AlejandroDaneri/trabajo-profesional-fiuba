package pythonservice

import (
	"bytes"
	"encoding/json"
	"io"
	"net/http"
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
	RunBacktesting(query BacktestingQuery) (BacktestingResponse, error)
	GetIndicators() (IndicatorsResponse, error)
}

type RiskValue struct {
    Value       float64 `json:"value"`
    Description string  `json:"description"`
}

type Risk struct {
    BuyAndHold map[string]RiskValue `json:"buy_and_hold"`
    Strategy   map[string]RiskValue `json:"strategy"`
}
type Trade struct {
    CumulativeReturn   float64 `json:"cumulative_return"`
    EntryDate          string  `json:"entry_date"`
    EntryPrice         float64 `json:"entry_price"`
    FixedCommission    float64 `json:"fixed_commission"`
    OutputDate         string  `json:"output_date"`
    OutputPrice        float64 `json:"output_price"`
    Result             string  `json:"result"`
    Return             float64 `json:"return"`
    VariableCommission float64 `json:"variable_commission"`
}

type SeriesEntry struct {
    Date              string  `json:"date"`
    BalanceStrategy   float64 `json:"balance_strategy"`
    BalanceBuyAndHold float64 `json:"balance_buy_and_hold"`
}


type BacktestingResponse map[string]struct {
    FinalBalance float64       `json:"final_balance"`
    Risks        Risk          `json:"risks"`
    Series       []SeriesEntry `json:"series"`
    Trades       []Trade       `json:"trades"`
}

type IndicatorsResponse []struct {
	Name       string                 `json:"name"`
	Parameters map[string]interface{} `json:"parameters"`
}

type BacktestingQuery struct {
	Coins          []string `json:"coins"`
	InitialBalance int      `json:"initial_balance"`
	DataFrom       int64    `json:"data_from"`
	DataTo         int64    `json:"data_to"`
	Type           string   `json:"type"`
	Strategy	   string   `json:"strategy"`
	Timeframe      string   `json:"timeframe"`
	Indicators     []struct {
		Name       string      `json:"name"`
		Parameters interface{} `json:"parameters"`
	} `json:"indicators"`
}

func (s *PythonService) RunBacktesting(query BacktestingQuery) (BacktestingResponse, error) {
	baseURL := "http://backtester:5000"
	endpoint := "backtest"

	url := baseURL + "/" + endpoint

	q, err := json.Marshal(query)
	if err != nil {
		logrus.WithFields(logrus.Fields{
			"err": err,
		}).Error("Could not unmarshal")
		return BacktestingResponse{}, err
	}

	response, err := http.Post(url, "application/json", bytes.NewBuffer(q))
	if err != nil {
		return BacktestingResponse{}, err
	}
	defer response.Body.Close()

	body, err := io.ReadAll(response.Body)
	if err != nil {
		return BacktestingResponse{}, err
	}

	var backtesting BacktestingResponse
	err = json.Unmarshal(body, &backtesting)
	if err != nil {
		logrus.WithFields(logrus.Fields{
			"err": err,
		}).Error("Could not unmarshal")
		return BacktestingResponse{}, err
	}
	return backtesting, nil
}

func (s *PythonService) GetIndicators() (IndicatorsResponse, error) {
	baseURL := "http://backtester:5000"
	endpoint := "indicators"

	url := baseURL + "/" + endpoint

	response, err := http.Get(url)
	if err != nil {
		return IndicatorsResponse{}, err
	}
	defer response.Body.Close()

	body, err := io.ReadAll(response.Body)
	if err != nil {
		return IndicatorsResponse{}, err
	}

	var indicators IndicatorsResponse
	err = json.Unmarshal(body, &indicators)
	if err != nil {
		logrus.WithFields(logrus.Fields{
			"err": err,
		}).Error("Could not unmarshal")
		return IndicatorsResponse{}, err
	}
	return indicators, nil
}
