package main

import (
	"algo_api/internal/tradeservice"
	"encoding/json"
	"fmt"
	"net/http"
	"time"

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
		Pair   string `json:"pair"`
		Price  string `json:"price"`
		Amount string `json:"amount"`
	}

	err := json.NewDecoder(r.Body).Decode(&body)
	if err != nil {
		logrus.Errorf("Credentials could not be decoded in request body: %v", err)
		http.Error(w, http.StatusText(400), 400)
		return
	}

	trade := map[string]interface{}{}

	trade["pair"] = body.Pair
	trade["price"] = body.Price
	trade["amount"] = body.Amount
	trade["timestamp"] = time.Now().Unix()

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

func main() {
	router := mux.NewRouter()

	router.HandleFunc("/ping", PingPong).Methods("GET")

	router.HandleFunc("/trade", CreateTrade).Methods("POST")
	router.HandleFunc("/trade/{tradeId}", GetTrade).Methods("GET")
	router.HandleFunc("/trade", ListTrades).Methods("GET")

	router.HandleFunc("/", handler)

	fmt.Println("Servidor escuchando en el puerto 8080")
	err := http.ListenAndServe(":8080", router)
	if err != nil {
		fmt.Println("Error al iniciar el servidor:", err)
	}
}
