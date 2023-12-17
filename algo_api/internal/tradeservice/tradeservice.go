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
	Create(trade map[string]interface{}) (string, error)
	Get(id string) (*database.TradePublicFields, error)
	List() ([]*database.TradePublicFields, error)
}

func (s *TradeService) Create(trade map[string]interface{}) (string, error) {
	dbName := "trades"
	db, err := s.databaseservice.GetDB(dbName)
	if err != nil {
		return "", err
	}
	trade["pvt_type"] = "trade"
	id, _, err := db.Save(trade, nil)
	if err != nil {
		return "", err
	}
	return id, nil
}

func (s *TradeService) Get(id string) (*database.TradePublicFields, error) {
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
	return &trade.TradePublicFields, nil
}

func (s *TradeService) List() ([]*database.TradePublicFields, error) {
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
	trades := []*database.TradePublicFields{}
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
		trades = append(trades, &trade.TradePublicFields)
	}
	return trades, nil
}
