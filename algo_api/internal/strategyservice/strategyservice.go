package strategyservice

import (
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
}

func NewService() IService {
	return &StrategyService{
		databaseservice: databaseservice.GetInstance(),
	}
}

type IService interface {
	GetRunning() (*database.StrategyResponseFields, error)
	List() ([]*database.StrategyResponseFields, error)
	SetInitialBalance(balance string) error
	SetCurrentBalance(balance string) error
	Start(strategy map[string]interface{}) (string, error)
	Stop(id string) error
	Delete() error
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

func (s *StrategyService) SetInitialBalance(balance string) error {
	strategy, err := s.get("")
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

func (s *StrategyService) SetCurrentBalance(balance string) error {
	strategy, err := s.get("")
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

func (s *StrategyService) Delete() error {
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
		if err != nil {
			continue
		}
	}

	return nil
}
