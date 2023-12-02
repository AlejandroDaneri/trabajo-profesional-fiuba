package tradeservice

import (
	"algo_api/databaseservice"
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
	Create(trade map[string]interface{}) error
}

func (s *TradeService) Create(trade map[string]interface{}) error {
	dbName := "trades"
	db, err := s.databaseservice.GetDB(dbName)
	if err != nil {
		return err
	}
	_, _, err = db.Save(trade, nil)
	if err != nil {
		return err
	}
	return nil
}
