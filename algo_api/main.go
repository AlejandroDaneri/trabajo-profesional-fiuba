package main

import (
	"algo_api/databaseservice"
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
	dbName := "trades"
	db, err := databaseservice.GetInstance().GetDB(dbName)
	if err != nil {
		logrus.WithFields(logrus.Fields{
			"err":     err,
			"db name": dbName,
		}).Error("Could not get DB")
		http.Error(w, http.StatusText(500), 500)
		return
	}
	doc := map[string]interface{}{
		"pair": "BTC/USDT",
	}
	_, _, err = db.Save(doc, nil)
	if err != nil {
		logrus.Error("Could not create doc")
		return
	}
}

func GetTrade(w http.ResponseWriter, r *http.Request) {
}

func ListTrades(w http.ResponseWriter, r *http.Request) {
}

func main() {
	router := mux.NewRouter()

	router.HandleFunc("/ping", PingPong).Methods("POST")

	router.HandleFunc("/trade", CreateTrade).Methods("POST")
	router.HandleFunc("/trade/{id}", GetTrade).Methods("GET")
	router.HandleFunc("/trade", ListTrades).Methods("GET")

	router.HandleFunc("/", handler)

	fmt.Println("Servidor escuchando en el puerto 8080")
	err := http.ListenAndServe(":8080", router)
	if err != nil {
		fmt.Println("Error al iniciar el servidor:", err)
	}
}
