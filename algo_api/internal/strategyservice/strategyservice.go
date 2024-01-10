package strategyservice

import (
	"algo_api/internal/database"
	"algo_api/internal/databaseservice"
	"algo_api/internal/utils"
	"encoding/json"
	"sync"
	"time"
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
	GetID() (string, error)
	Get() (*database.StrategyPublicFields, error)
	SetCurrentBalance(balance string) error
	Start(strategy map[string]interface{}) (string, error)
	Stop(id string) error
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

func (s *StrategyService) GetID() (string, error) {
	strategy, err := s.get()
	if err != nil {
		return "", err
	}
	return strategy.ID, nil
}

func (s *StrategyService) SetCurrentBalance(balance string) error {
	strategy, err := s.get()
	if err != nil {
		return err
	}

	strategy.CurrentBalance = balance

	m, err := utils.StructToMap(*strategy)
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

func (s *StrategyService) Start(strategy map[string]interface{}) (string, error) {
	dbName := "trades"
	db, err := s.databaseservice.GetDB(dbName)
	if err != nil {
		return "", err
	}
	strategy["pvt_type"] = "strategy"
	strategy["state"] = database.StrategyStateRunning
	strategy["start_timestamp"] = time.Now().Unix()
	id, _, err := db.Save(strategy, nil)
	if err != nil {
		return "", err
	}
	return id, nil
}

func (s *StrategyService) Stop(id string) error {
	strategy, err := s.get()
	if err != nil {
		return err
	}
	strategy.State = database.StrategyStateFinished
	strategy.EndTimestamp = time.Now().Unix()

	m, err := utils.StructToMap(*strategy)
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
