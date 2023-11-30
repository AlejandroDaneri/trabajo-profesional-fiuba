package main

import (
	"encoding/json"
	"fmt"
	"net/http"

	"github.com/gorilla/mux"
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
