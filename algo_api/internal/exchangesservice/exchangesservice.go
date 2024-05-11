package exchangesservice

import (
	"algo_api/internal/database"
	"algo_api/internal/databaseservice"
	"encoding/json"
	"errors"
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

type ExchangesService struct {
	databaseservice databaseservice.IService
}

func NewService() IService {
	return &ExchangesService{
		databaseservice: databaseservice.GetInstance(),
	}
}

type IService interface {
	AddExchange(exchangeName string, apiKey string, apiSecret string, alias string, testingNetwork bool) error
	GetExchanges() ([]*database.ExchangeResponseFields, error)
	DeleteExchange(exchangeName string, apiKey string, testingNetwork bool) error
}

func (t *ExchangesService) AddExchange(exchangeName string, apiKey string, apiSecret string, alias string, testingNetwork bool) error {
	exchange := make(map[string]interface{})
	dbName := "exchanges"
	db, err := t.databaseservice.GetDB(dbName)
	if err != nil {
		return err
	}
	exchange["type"] = exchangeName
	exchange["api_key"] = apiKey
	exchange["api_secret"] = apiSecret
	exchange["alias"] = alias
	exchange["testing_network"] = testingNetwork
	exchange["pvt_type"] = "exchange"
	_, _, err = db.Save(exchange, nil)
	if err != nil {
		return err
	}
	return nil
}

func (t *ExchangesService) GetExchanges() ([]*database.ExchangeResponseFields, error) {
	dbName := "exchanges"
	db, err := t.databaseservice.GetDB(dbName)
	if err != nil {
		return nil, err
	}
	q := `
    {
        "selector": {
            "pvt_type": "exchange"
        }
    }
    `
	docs, err := db.QueryJSON(q)
	if err != nil {
		return nil, err
	}
	exchanges := []*database.ExchangeResponseFields{}
	for _, doc := range docs {
		bytes, err := json.Marshal(doc)
		if err != nil {
			continue
		}
		exchange := database.Exchange{}
		err = json.Unmarshal(bytes, &exchange)
		if err != nil {
			continue
		}
		exchanges = append(exchanges, &database.ExchangeResponseFields{
			ExchangePublicFields: exchange.ExchangePublicFields,
			ID:                   exchange.ID,
		})
	}
	return exchanges, nil
}

func (t *ExchangesService) DeleteExchange(exchangeName string, apiKey string, testingNetwork bool) error {
	dbName := "exchanges"
	db, err := t.databaseservice.GetDB(dbName)
	if err != nil {
		return err
	}

	q := fmt.Sprintf(`
        {
            "selector": {
                "type": "%s",
                "api_key": "%s",
                "testing_network": %t,
                "pvt_type": "exchange"
            }
        }
    `, exchangeName, apiKey, testingNetwork)

	docs, err := db.QueryJSON(q)
	if err != nil {
		return err
	}

	if len(docs) == 0 {
		return errors.New("desired exchange not found")
	}

	for _, doc := range docs {
		id := doc["_id"].(string)
		err := db.Delete(id)
		if err != nil {
			return err
		}
	}

	return nil
}
