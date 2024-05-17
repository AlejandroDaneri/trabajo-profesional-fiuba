package tradeservice

import (
	"algo_api/internal/database"
	"algo_api/internal/databaseservice"
	"algo_api/internal/utils"
	"encoding/json"
	"fmt"
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
	GetOpen() (*database.Trade, error)
	Close(price string) error
	ListAll() ([]*database.TradeResponseFields, error)
	ListByStrategy(strategyID string) ([]*database.TradeResponseFields, error)
	Remove(id string) error
	RemoveAll() error
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

func (s *TradeService) GetOpen() (*database.Trade, error) {
	dbName := "trades"
	db, err := s.databaseservice.GetDB(dbName)
	if err != nil {
		return nil, err
	}
	q := `
	{
		"selector": {
			"pvt_type": "trade",
			"orders.sell.price": {
				"$exists": false
			},
			"orders.sell.timestamp": {
				"$exists": false
			}
		},
		"limit": 10000
	}
	`
	docs, err := db.QueryJSON(q)
	if err != nil {
		return nil, err
	}
	if len(docs) == 0 {
		return nil, nil
	}
	trade := database.Trade{}
	for _, doc := range docs {
		bytes, err := json.Marshal(doc)
		if err != nil {
			return nil, err
		}
		err = json.Unmarshal(bytes, &trade)
		if err != nil {
			return nil, err
		}

	}
	return &trade, nil
}

func (s *TradeService) Close(price string) error {
	trade, err := s.GetOpen()
	if err != nil {
		return err
	}

	trade.Orders.Sell = database.TradePublicSell{}
	trade.Orders.Sell.Price = price
	trade.Orders.Sell.Timestamp = time.Now().Unix()

	dbName := "trades"
	db, err := s.databaseservice.GetDB(dbName)
	if err != nil {
		return err
	}
	doc, err := utils.StructToMap(trade)
	if err != nil {
		return err
	}
	_, _, err = db.Save(doc, nil)
	if err != nil {
		return err
	}
	return nil
}

func (s *TradeService) ListAll() ([]*database.TradeResponseFields, error) {
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

func (s *TradeService) ListByStrategy(strategyID string) ([]*database.TradeResponseFields, error) {
	dbName := "trades"
	db, err := s.databaseservice.GetDB(dbName)
	if err != nil {
		return nil, err
	}
	q := fmt.Sprintf(`
	{
		"selector": {
			"pvt_type": "trade",
			"strategy_id": "%s"
		},
		"limit": 10000
	}
	`, strategyID)
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

func (s *TradeService) Remove(id string) error {
	dbName := "trades"
	db, err := s.databaseservice.GetDB(dbName)
	if err != nil {
		return err
	}

	err = db.Delete(id)
	if err != nil {
		return err
	}

	return nil
}

func (s *TradeService) RemoveAll() error {
	dbName := "trades"
	db, err := s.databaseservice.GetDB(dbName)
	if err != nil {
		return err
	}

	trades, err := s.ListAll()
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
