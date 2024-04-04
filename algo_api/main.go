package main

import (
	"algo_api/internal/strategyservice"
	"algo_api/internal/telegramservice"
	"algo_api/internal/tradeservice"
	"algo_api/internal/utils"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"strconv"

	"github.com/getsentry/sentry-go"
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
		logrus.WithFields(logrus.Fields{
			"err": err,
		}).Error("Could not decode body")
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

	strategy, err := strategyservice.GetInstance().GetRunning()
	if err != nil {
		logrus.WithFields(logrus.Fields{
			"err": err,
		}).Error("Could not get the strategy")
		return
	}

	id, err := tradeservice.GetInstance().Create(trade, strategy.ID)
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

func RemoveCurrentTrade(w http.ResponseWriter, r *http.Request) {
	err := tradeservice.GetInstance().Remove("current")
	if err != nil {
		logrus.WithFields(logrus.Fields{
			"err": err,
		}).Error("Could not delete current trade")
		return
	}
}

func GetCurrentTrade(w http.ResponseWriter, r *http.Request) {
	id := "current"

	currentTrade, err := tradeservice.GetInstance().Get(id)
	if err != nil {
		logrus.WithFields(logrus.Fields{
			"err": err,
		}).Error("Could not get current trade")
		http.Error(w, http.StatusText(400), 400)
		return
	}

	bytes, err := json.Marshal(currentTrade)
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

func SetCurrentTrade(w http.ResponseWriter, r *http.Request) {
	var body struct {
		Pair     string `json:"pair"`
		Amount   string `json:"amount"`
		BuyOrder struct {
			Price     string `json:"price"`
			Timestamp int64  `json:"timestamp"`
		} `json:"buy"`
	}

	err := json.NewDecoder(r.Body).Decode(&body)
	if err != nil {
		logrus.WithFields(logrus.Fields{
			"err": err,
		}).Error("Could not decode body")
		http.Error(w, http.StatusText(400), 400)
		return
	}

	id := "current"

	trade := map[string]interface{}{
		"_id":    id,
		"pair":   body.Pair,
		"amount": body.Amount,
		"orders": map[string]interface{}{
			"buy": map[string]interface{}{
				"price":     body.BuyOrder.Price,
				"timestamp": body.BuyOrder.Timestamp,
			},
		},
		"type": "trade",
	}

	strategy, err := strategyservice.GetInstance().GetRunning()
	if err != nil {
		logrus.WithFields(logrus.Fields{
			"err": err,
		}).Error("Could not get the strategy")
		return
	}

	currentTrade, err := tradeservice.GetInstance().Get(id)
	if err != nil {
		logrus.WithFields(logrus.Fields{
			"err": err,
		}).Error("Could not get current trade")
	}

	if currentTrade != nil {
		err := tradeservice.GetInstance().Remove(id)
		if err != nil {
			logrus.WithFields(logrus.Fields{
				"err": err,
			}).Error("Could not delete current trade")
			return
		}
	}

	_, err = tradeservice.GetInstance().Create(trade, strategy.ID)
	if err != nil {
		logrus.WithFields(logrus.Fields{
			"err": err,
		}).Error("Could not create current trade")
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
	vars := mux.Vars(r)
	strategyId := vars["strategyId"]
	logrus.Info(strategyId)
	if strategyId == "" {
		logrus.Error("Could not get strategy id")
		http.Error(w, http.StatusText(400), 400)
		return
	}
	trades, err := tradeservice.GetInstance().ListByStrategy(strategyId)
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
	err := tradeservice.GetInstance().RemoveAll()
	if err != nil {
		logrus.WithFields(logrus.Fields{
			"err": err,
		}).Error("Could not remove trades")
		http.Error(w, http.StatusText(500), 500)
		return
	}
}

func GetRunningStrategy(w http.ResponseWriter, r *http.Request) {
	strategy, err := strategyservice.GetInstance().GetRunning()
	if err != nil {
		logrus.WithFields(logrus.Fields{
			"err": err,
		}).Error("Could not get find strategy running")
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

func SetStrategyInitialBalance(w http.ResponseWriter, r *http.Request) {
	var body struct {
		InitialBalance string `json:"initial_balance"`
	}

	err := json.NewDecoder(r.Body).Decode(&body)
	if err != nil {
		logrus.WithFields(logrus.Fields{
			"err": err,
		}).Error("Could not decode body")
		http.Error(w, http.StatusText(400), 400)
		return
	}

	err = strategyservice.GetInstance().SetInitialBalance(body.InitialBalance)
	if err != nil {
		logrus.Error("Could not set balance to the strategy")
		http.Error(w, http.StatusText(500), 500)
		return
	}
}

func SetStrategyBalance(w http.ResponseWriter, r *http.Request) {
	var body struct {
		CurrentBalance string `json:"current_balance"`
	}

	err := json.NewDecoder(r.Body).Decode(&body)
	if err != nil {
		logrus.WithFields(logrus.Fields{
			"err": err,
		}).Error("Could not decode body")
		http.Error(w, http.StatusText(400), 400)
		return
	}

	err = strategyservice.GetInstance().SetCurrentBalance(body.CurrentBalance)
	if err != nil {
		logrus.Error("Could not set balance to the strategy")
		http.Error(w, http.StatusText(500), 500)
		return
	}
}

func StopStrategy(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	id := vars["id"]
	err := strategyservice.GetInstance().Stop(id)
	if err != nil {
		logrus.WithFields(logrus.Fields{
			"err": err,
			"id":  id,
		}).Error("Could not stop the strategy")
		http.Error(w, http.StatusText(500), 500)
		return
	}
}

func CreateStrategy(w http.ResponseWriter, r *http.Request) {
	var body struct {
		InitialBalance string `json:"initial_balance"`
		Indicators     []struct {
			Name       string      `json:"name"`
			Parameters interface{} `json:"parameters"`
		} `json:"indicators"`
		Currencies []string `json:"currencies"`
	}

	err := json.NewDecoder(r.Body).Decode(&body)
	if err != nil {
		logrus.WithFields(logrus.Fields{
			"err": err,
		}).Error("Could not decode body")
		http.Error(w, http.StatusText(400), 400)
		return
	}

	strategy, err := utils.StructToMap(body)
	if err != nil {
		http.Error(w, http.StatusText(500), 500)
		return
	}

	id, err := strategyservice.GetInstance().Start(strategy)
	if err != nil {
		logrus.WithFields(logrus.Fields{
			"err": err,
			"id":  id,
		}).Error("Could not create the strategy")
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

func ListStrategy(w http.ResponseWriter, r *http.Request) {
	strategies, err := strategyservice.GetInstance().List()
	if err != nil {
		logrus.WithFields(logrus.Fields{
			"err": err,
		}).Error("Could not get strategies")
		http.Error(w, http.StatusText(500), 500)
		return
	}
	bytes, err := json.Marshal(strategies)
	if err != nil {
		logrus.WithFields(logrus.Fields{
			"err": err,
		}).Error("Could not marshall")
		http.Error(w, http.StatusText(500), 500)
		return
	}
	w.Write(bytes)
}

func DeleteStrategy(w http.ResponseWriter, r *http.Request) {
	err := strategyservice.GetInstance().Delete()
	if err != nil {
		logrus.WithFields(logrus.Fields{
			"err": err,
		}).Error("Could not delete strategies")
		http.Error(w, http.StatusText(500), 500)
		return
	}
}

func AddTelegramChat(w http.ResponseWriter, r *http.Request) {
	var body struct {
		ChatID int64 `json:"chat_id"`
	}

	err := json.NewDecoder(r.Body).Decode(&body)
	if err != nil {
		logrus.WithFields(logrus.Fields{
			"err": err,
		}).Error("Could not decode body")
		http.Error(w, http.StatusText(400), 400)
		return
	}

	err = telegramservice.GetInstance().AddTelegramChat(strconv.FormatInt(body.ChatID, 10))
	if err != nil {
		logrus.WithFields(logrus.Fields{
			"err": err,
		}).Error("Could not add Telegram chat ID")
		http.Error(w, http.StatusText(500), 500)
		return
	}

	response := map[string]string{"message": "Telegram chat ID added successfully"}
	bytes, err := json.Marshal(response)
	if err != nil {
		http.Error(w, http.StatusText(500), 500)
		return
	}

	w.WriteHeader(http.StatusCreated)
	w.Write(bytes)
}

func GetTelegramChats(w http.ResponseWriter, r *http.Request) {
	chats, err := telegramservice.GetInstance().GetAllTelegramChats()
	if err != nil {
		logrus.WithError(err).Error("Failed to get Telegram chats")
		http.Error(w, http.StatusText(http.StatusInternalServerError), http.StatusInternalServerError)
		return
	}

	response, err := json.Marshal(chats)
	if err != nil {
		logrus.WithError(err).Error("Failed to marshal response")
		http.Error(w, http.StatusText(http.StatusInternalServerError), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	_, err = w.Write(response)
	if err != nil {
		logrus.WithError(err).Error("Failed to write response")
	}
}

func MakeRoutes(router *mux.Router) {
	router.HandleFunc("/trade", CreateTrade).Methods("POST")
	router.HandleFunc("/trade/current", GetCurrentTrade).Methods("GET")
	router.HandleFunc("/trade/current", SetCurrentTrade).Methods("PUT")
	router.HandleFunc("/trade/current", RemoveCurrentTrade).Methods("DELETE")
	router.HandleFunc("/trade/{tradeId}", GetTrade).Methods("GET")
	router.HandleFunc("/trades/strategy/{strategyId}", ListTrades).Methods("GET")
	router.HandleFunc("/trade", RemoveTrades).Methods("DELETE")

	router.HandleFunc("/strategy/running", GetRunningStrategy).Methods("GET")
	router.HandleFunc("/strategy", ListStrategy).Methods("GET")
	router.HandleFunc("/strategy", DeleteStrategy).Methods("DELETE")
	router.HandleFunc("/strategy/initial_balance", SetStrategyInitialBalance).Methods("PUT")
	router.HandleFunc("/strategy/balance", SetStrategyBalance).Methods("PUT")
	router.HandleFunc("/strategy/stop/{id}", StopStrategy).Methods("PUT")
	router.HandleFunc("/strategy", CreateStrategy).Methods("POST")

	router.HandleFunc("/telegram/chat", AddTelegramChat).Methods("POST")
	router.HandleFunc("/telegram/chats", GetTelegramChats).Methods("GET")
}

func main() {
	myVar := os.Getenv("ENV")
	if myVar != "development" {
		err := sentry.Init(sentry.ClientOptions{
			Dsn: "https://23953c767ab38badfb11e0f1e37181ca@o4506996875919360.ingest.us.sentry.io/4507018359078912",
			// Set TracesSampleRate to 1.0 to capture 100%
			// of transactions for performance monitoring.
			// We recommend adjusting this value in production,
			TracesSampleRate: 1.0,
		})
		if err != nil {
			log.Fatalf("sentry.Init: %s", err)
		}
	}

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
