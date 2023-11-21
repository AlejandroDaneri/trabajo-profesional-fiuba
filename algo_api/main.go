package main

import (
	"encoding/json"
	"fmt"
	"net/http"
)

func handler(w http.ResponseWriter, r *http.Request) {
}

func handlerPing(w http.ResponseWriter, r *http.Request) {
	response, err := json.Marshal("pong")
	if err != nil {
		return
	}

	w.Write(response)
}

func main() {
	http.HandleFunc("/ping", handlerPing)
	http.HandleFunc("/", handler)

	fmt.Println("Servidor escuchando en el puerto 8080")
	err := http.ListenAndServe(":8080", nil)
	if err != nil {
		fmt.Println("Error al iniciar el servidor:", err)
	}
}
