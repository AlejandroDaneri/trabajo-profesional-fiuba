package main

import (
	"algo_api/internal/databaseservice"

	"github.com/sirupsen/logrus"
)

// go run cmd/setup/main.go
// example how to run commands on go
func main() {
	logrus.Info("Setup DB")
	err := databaseservice.GetInstance().CreateDB("trades")
	if err != nil {
		logrus.Error("Could not create DB")
	}
}
