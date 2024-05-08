package strategyservice

import (
	"algo_api/internal/binanceservice"
	"algo_api/internal/database"
	"algo_api/internal/databaseservice"
	"algo_api/internal/utils"
	"encoding/json"
	"errors"
	"fmt"
	"sync"
	"time"

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

type StrategyService struct {
	databaseservice databaseservice.IService
	binanceservice  binanceservice.IService
}

func NewService() IService {
	return &StrategyService{
		databaseservice: databaseservice.GetInstance(),
		binanceservice:  binanceservice.GetInstance(),
	}
}

type IService interface {
	GetRunning() (*database.StrategyResponseFields, error)
	List() ([]*database.StrategyResponseFields, error)
	SetInitialBalance(id, balance string) error
	SetCurrentBalance(id, balance string) error
	Get(id string) (*database.StrategyResponseFields, error)
	Create(strategy map[string]interface{}) (string, error)
	Start(id string) error
	Stop(id string) error
	DeleteAll() error
	Delete(id string) error
}

func (s *StrategyService) get(id string) (*database.Strategy, error) {
	dbName := "trades"
	db, err := s.databaseservice.GetDB(dbName)
	if err != nil {
		return nil, err
	}
	var q string
	if id == "" {
		q = fmt.Sprintf(`{
			"selector": {
				"state": "%s",
				"pvt_type": "strategy"
			},
			"limit": 1
		}`, database.StrategyStateRunning)
	} else {
		q = fmt.Sprintf(`
		{
			"selector": {
				"_id": "%s",
				"pvt_type": "strategy"
			},
			"limit": 1
		}`, id)
	}
	docs, err := db.QueryJSON(q)
	if err != nil {
		logrus.WithFields(logrus.Fields{
			"err": err,
			"q":   utils.ToPrettyPrint(q),
		}).Error("Could not run the Mango Query")
		return nil, err
	}
	if len(docs) == 0 {
		return nil, errors.New("could not find any running strategy")
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

func (s *StrategyService) GetRunning() (*database.StrategyResponseFields, error) {
	strategy, err := s.get("")
	if err != nil {
		return nil, err
	}

	balance, err := s.binanceservice.GetBalance()
	if err != nil {
		return nil, err
	}

	strategy.CurrentBalance = balance

	return &database.StrategyResponseFields{
		StrategyPublicFields: strategy.StrategyPublicFields,
		ID:                   strategy.ID,
	}, nil
}

func (s *StrategyService) Get(id string) (*database.StrategyResponseFields, error) {
	strategy, err := s.get(id)
	if err != nil {
		return nil, err
	}

	return &database.StrategyResponseFields{
		StrategyPublicFields: strategy.StrategyPublicFields,
		ID:                   strategy.ID,
	}, nil
}

func (s *StrategyService) List() ([]*database.StrategyResponseFields, error) {
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
		"limit": 10000
	}
	`
	docs, err := db.QueryJSON(q)
	if err != nil {
		return nil, err
	}
	strategies := []*database.StrategyResponseFields{}
	for _, doc := range docs {
		bytes, err := json.Marshal(doc)
		if err != nil {
			continue
		}
		strategy := database.Strategy{}
		err = json.Unmarshal(bytes, &strategy)
		if err != nil {
			continue
		}
		strategies = append(strategies, &database.StrategyResponseFields{
			StrategyPublicFields: strategy.StrategyPublicFields,
			ID:                   strategy.ID,
		})
	}
	return strategies, nil
}

func (s *StrategyService) SetInitialBalance(id, balance string) error {
	strategy, err := s.get(id)
	if err != nil {
		return err
	}

	strategy.InitialBalance = balance

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

func (s *StrategyService) SetCurrentBalance(id, balance string) error {
	strategy, err := s.get(id)
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

func (s *StrategyService) Create(strategy map[string]interface{}) (string, error) {
	dbName := "trades"
	db, err := s.databaseservice.GetDB(dbName)
	if err != nil {
		return "", err
	}
	strategy["pvt_type"] = "strategy"
	strategy["type"] = "basic"
	strategy["state"] = database.StrategyStateCreated
	strategy["exchange"] = "binance"
	id, _, err := db.Save(strategy, nil)
	if err != nil {
		return "", err
	}
	return id, nil
}

func (s *StrategyService) Stop(id string) error {
	strategy, err := s.get(id)
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

func (s *StrategyService) Start(id string) error {
	strategy, err := s.get(id)
	if err != nil {
		return err
	}
	strategy.State = database.StrategyStateRunning
	strategy.StartTimestamp = time.Now().Unix()

	balance, err := s.binanceservice.GetBalance()
	if err != nil {
		return err
	}
	strategy.InitialBalance = balance
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

func (s *StrategyService) DeleteAll() error {
	dbName := "trades"
	db, err := s.databaseservice.GetDB(dbName)
	if err != nil {
		return err
	}

	strategies, err := s.List()
	if err != nil {
		return err
	}

	for _, strategy := range strategies {
		err = db.Delete(strategy.ID)
	}

	return err
}

func (s *StrategyService) Delete(id string) error {
	dbName := "trades"
	db, err := s.databaseservice.GetDB(dbName)
	if err != nil {
		return err
	}

	err = db.Delete(id)

	return err
}
