package tradeservice

import (
	"algo_api/internal/database"
	"algo_api/internal/databaseservice"
	"encoding/json"
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

type TradeService struct {
	databaseservice databaseservice.IService
}

func NewService() IService {
	return &TradeService{
		databaseservice: databaseservice.GetInstance(),
	}
}

type IService interface {
	Create(trade map[string]interface{}, strategyID string) (string, error)
	Get(id string) (*database.TradeResponseFields, error)
	List() ([]*database.TradeResponseFields, error)
	Remove() error
}

func (s *TradeService) Create(trade map[string]interface{}, strategyID string) (string, error) {
	dbName := "trades"
	db, err := s.databaseservice.GetDB(dbName)
	if err != nil {
		return "", err
	}
	trade["strategy_id"] = strategyID
	trade["pvt_type"] = "trade"
	id, _, err := db.Save(trade, nil)
	if err != nil {
		return "", err
	}
	return id, nil
}

func (s *TradeService) Get(id string) (*database.TradeResponseFields, error) {
	dbName := "trades"
	db, err := s.databaseservice.GetDB(dbName)
	if err != nil {
		return nil, err
	}
	doc, err := db.Get(id, nil)
	if err != nil {
		return nil, err
	}
	bytes, err := json.Marshal(doc)
	if err != nil {
		return nil, err
	}
	var trade *database.Trade
	err = json.Unmarshal(bytes, &trade)
	if err != nil {
		return nil, err
	}
	return &database.TradeResponseFields{
		TradePublicFields: trade.TradePublicFields,
		ID:                trade.ID,
	}, nil
}

func (s *TradeService) List() ([]*database.TradeResponseFields, error) {
	dbName := "trades"
	db, err := s.databaseservice.GetDB(dbName)
	if err != nil {
		return nil, err
	}
	q := `
	{
		"selector": {
			"pvt_type": "trade"
		},
		"limit": 10000
	}
	`
	docs, err := db.QueryJSON(q)
	if err != nil {
		return nil, err
	}
	trades := []*database.TradeResponseFields{}
	for _, doc := range docs {
		bytes, err := json.Marshal(doc)
		if err != nil {
			continue
		}
		trade := database.Trade{}
		err = json.Unmarshal(bytes, &trade)
		if err != nil {
			continue
		}
		trades = append(trades, &database.TradeResponseFields{
			TradePublicFields: trade.TradePublicFields,
			ID:                trade.ID,
		})
	}
	return trades, nil
}

func (s *TradeService) Remove() error {
	dbName := "trades"
	db, err := s.databaseservice.GetDB(dbName)
	if err != nil {
		return err
	}

	trades, err := s.List()
	if err != nil {
		return err
	}

	for _, trade := range trades {
		err = db.Delete(trade.ID)
		if err != nil {
			continue
		}
	}

	return nil
}
