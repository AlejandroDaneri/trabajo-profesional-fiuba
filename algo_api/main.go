package main

import (
	"algo_api/internal/strategyservice"
	"algo_api/internal/tradeservice"
	"encoding/json"
	"fmt"
	"net/http"

	"github.com/gorilla/mux"
	"github.com/sirupsen/logrus"
)

func handler(w http.ResponseWriter, r *http.Request) {
}

func PingPong(w http.ResponseWriter, r *http.Request) {
	response, err := json.Marshal("pong")
	if err != nil {
		return
	}

	w.Write(response)
}

func CreateTrade(w http.ResponseWriter, r *http.Request) {
	var body struct {
		Pair     string `json:"pair"`
		Amount   string `json:"amount"`
		BuyOrder struct {
			Price     string `json:"price"`
			Timestamp int64  `json:"timestamp"`
		} `json:"buy"`
		SellOrder struct {
			Price     string `json:"price"`
			Timestamp int64  `json:"timestamp"`
		} `json:"sell"`
	}

	err := json.NewDecoder(r.Body).Decode(&body)
	if err != nil {
		logrus.Errorf("Credentials could not be decoded in request body: %v", err)
		http.Error(w, http.StatusText(400), 400)
		return
	}

	trade := map[string]interface{}{
		"pair":   body.Pair,
		"amount": body.Amount,
		"orders": map[string]interface{}{
			"buy": map[string]interface{}{
				"price":     body.BuyOrder.Price,
				"timestamp": body.BuyOrder.Timestamp,
			},
			"sell": map[string]interface{}{
				"price":     body.SellOrder.Price,
				"timestamp": body.SellOrder.Timestamp,
			},
		},
	}

	id, err := tradeservice.GetInstance().Create(trade)
	if err != nil {
		logrus.WithFields(logrus.Fields{
			"err":   err,
			"trade": trade,
		}).Error("Could not create the trade")
		http.Error(w, http.StatusText(500), 500)
		return
	}

	bytes, err := json.Marshal(id)
	if err != nil {
		http.Error(w, http.StatusText(500), 500)
		return
	}

	_, err = w.Write(bytes)
	if err != nil {
		http.Error(w, http.StatusText(500), 500)
		return
	}
}

func GetTrade(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	tradeID := vars["tradeId"]
	if tradeID == "" {
		logrus.Error("Could not get trade id")
		http.Error(w, http.StatusText(400), 400)
		return
	}
	trade, err := tradeservice.GetInstance().Get(tradeID)
	if err != nil {
		logrus.WithFields(logrus.Fields{
			"err":      err,
			"trade id": tradeID,
		}).Error("Could not get the trade")
		http.Error(w, http.StatusText(500), 500)
		return
	}
	bytes, err := json.Marshal(trade)
	if err != nil {
		logrus.WithFields(logrus.Fields{
			"err":      err,
			"trade id": tradeID,
		}).Error("Could not marshall")
		http.Error(w, http.StatusText(500), 500)
		return
	}
	_, err = w.Write(bytes)
	if err != nil {
		logrus.WithFields(logrus.Fields{
			"err":      err,
			"trade id": tradeID,
		}).Error("Could not write response")
		http.Error(w, http.StatusText(500), 500)
	}
}

func ListTrades(w http.ResponseWriter, r *http.Request) {
	trades, err := tradeservice.GetInstance().List()
	if err != nil {
		logrus.WithFields(logrus.Fields{
			"err": err,
		}).Error("Could not get trades")
		http.Error(w, http.StatusText(500), 500)
		return
	}
	bytes, err := json.Marshal(trades)
	if err != nil {
		logrus.WithFields(logrus.Fields{
			"err": err,
		}).Error("Could not marshall")
		http.Error(w, http.StatusText(500), 500)
		return
	}
	w.Write(bytes)
}

func RemoveTrades(w http.ResponseWriter, r *http.Request) {
	err := tradeservice.GetInstance().Remove()
	if err != nil {
		logrus.WithFields(logrus.Fields{
			"err": err,
		}).Error("Could not remove trades")
		http.Error(w, http.StatusText(500), 500)
		return
	}
}

func GetStrategy(w http.ResponseWriter, r *http.Request) {
	strategy, err := strategyservice.GetInstance().Get()
	if err != nil {
		logrus.WithFields(logrus.Fields{
			"err": err,
		}).Error("Could not get the strategy")
		http.Error(w, http.StatusText(500), 500)
		return
	}
	bytes, err := json.Marshal(strategy)
	if err != nil {
		logrus.WithFields(logrus.Fields{
			"err": err,
		}).Error("Could not marshall")
		http.Error(w, http.StatusText(500), 500)
		return
	}
	_, err = w.Write(bytes)
	if err != nil {
		logrus.WithFields(logrus.Fields{
			"err": err,
		}).Error("Could not write response")
		http.Error(w, http.StatusText(500), 500)
	}
}

func SetStrategyBalance(w http.ResponseWriter, r *http.Request) {
	balance := 40
	err := strategyservice.GetInstance().SetBalance(balance)
	if err != nil {
		logrus.Error("Could not set balance to the strategy")
		http.Error(w, http.StatusText(500), 500)
		return
	}
}

func MakeRoutes(router *mux.Router) {
	router.HandleFunc("/trade", CreateTrade).Methods("POST")
	router.HandleFunc("/trade/{tradeId}", GetTrade).Methods("GET")
	router.HandleFunc("/trade", ListTrades).Methods("GET")
	router.HandleFunc("/trade", RemoveTrades).Methods("DELETE")

	router.HandleFunc("/strategy", GetStrategy).Methods("GET")
	router.HandleFunc("/strategy/balance", SetStrategyBalance).Methods("PUT")
}

func main() {
	router := mux.NewRouter()
	apiRouter := router.PathPrefix("/api").Subrouter()
	MakeRoutes(apiRouter)

	router.HandleFunc("/ping", PingPong).Methods("GET")

	fmt.Println("Servidor escuchando en el puerto 8080")
	err := http.ListenAndServe(":8080", router)
	if err != nil {
		fmt.Println("Error al iniciar el servidor:", err)
	}
}
