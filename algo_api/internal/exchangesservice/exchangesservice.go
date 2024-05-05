package exchangesservice

import (
	"algo_api/internal/databaseservice"
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

type ExchangesService struct {
    databaseservice databaseservice.IService
}

func NewService() IService {
    return &ExchangesService{
        databaseservice: databaseservice.GetInstance(),
    }
}

type IService interface {
    AddExchange(exchangeName string, apiKey string, apiSecret string) (error)
}

func (t *ExchangesService) AddExchange(exchangeName string, apiKey string, apiSecret string) (error) {
    exchange := make(map[string]interface{})
    dbName := "exchanges"
    db, err := t.databaseservice.GetDB(dbName)
    if err != nil {
        return err
    }
    exchange["type"] = exchangeName
	exchange["api_key"] = apiKey
	exchange["api_secret"] = apiSecret
	exchange["pvt_type"] = "exchange"
    _, _, err = db.Save(exchange, nil)
    if err != nil {
        return err
    }
    return nil
}

