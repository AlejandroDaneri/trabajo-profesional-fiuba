package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"

	"github.com/gorilla/mux"
	"github.com/leesper/couchdb-golang"
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
	couchDBUser := os.Getenv("COUCHDB_USER")
	couchDBPassword := os.Getenv("COUCHDB_PASSWORD")
	client, err := couchdb.NewServer(fmt.Sprintf("http://%s:%s@couchdb:5984", couchDBUser, couchDBPassword))
	if err != nil {
		fmt.Println("Error al conectar a CouchDB:", err)
		return
	}
	dbName := "trades"
	db, err := client.Get(dbName)
	if err != nil {
		logrus.Error("Could not get db")
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
