package strategyservice

import (
	"algo_api/internal/database"
	"algo_api/internal/databaseservice"
	"encoding/json"
	"fmt"
	"sync"
)

var instance IService
var once sync.Once

func GetInstance() IService {
	once.Do(func() {
		instance = NewService()
	})
	return instance
}

type StrategyService struct {
	databaseservice databaseservice.IService
}

func NewService() IService {
	return &StrategyService{
		databaseservice: databaseservice.GetInstance(),
	}
}

type IService interface {
	Get() (*database.StrategyPublicFields, error)
	SetBalance(balance int) error
}

func (s *StrategyService) get() (*database.Strategy, error) {
	dbName := "trades"
	db, err := s.databaseservice.GetDB(dbName)
	if err != nil {
		return nil, err
	}
	q := `
	{
		"selector": {
			"pvt_type": "strategy"
		},
		"limit": 1
	}
	`
	docs, err := db.QueryJSON(q)
	if err != nil {
		return nil, err
	}
	bytes, err := json.Marshal(docs[0])
	if err != nil {
		return nil, err
	}
	var strategy *database.Strategy
	err = json.Unmarshal(bytes, &strategy)
	if err != nil {
		return nil, err
	}
	return strategy, nil
}

func (s *StrategyService) Get() (*database.StrategyPublicFields, error) {
	strategy, err := s.get()
	if err != nil {
		return nil, err
	}

	return &strategy.StrategyPublicFields, nil
}

func StructToMap(value interface{}) (map[string]interface{}, error) {
	if res, ok := value.(map[string]interface{}); ok {
		return res, nil
	}

	valueBytes, err := json.Marshal(value)
	if err != nil {
		return nil, fmt.Errorf("error marshalling struct: %w", err)
	}

	var valueMap map[string]interface{}
	err = json.Unmarshal(valueBytes, &valueMap)
	if err != nil {
		return nil, fmt.Errorf("error unmarshalling struct: %w", err)
	}

	return valueMap, nil
}

func ToPrettyPrint(m interface{}) string {
	b, err := json.MarshalIndent(m, "", "    ")
	if err == nil {
		return string(b)
	}
	return ""
}

func (s *StrategyService) SetBalance(balance int) error {
	strategy, err := s.get()
	if err != nil {
		return err
	}

	strategy.CurrentBalance = balance

	m, err := StructToMap(*strategy)
	if err != nil {
		return err
	}

	db, err := s.databaseservice.GetDB("trades")
	if err != nil {
		return err
	}

	_, _, err = db.Save(m, nil)
	if err != nil {
		return err
	}

	return nil
}
