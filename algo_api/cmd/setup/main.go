package main

import (
	"algo_api/internal/databaseservice"

	"github.com/sirupsen/logrus"
)

// go run cmd/setup/main.go
// initialize db
func main() {
	logrus.Info("Setup DB")

	err := databaseservice.GetInstance().CreateDB("_users")
	if err != nil {
		logrus.Error("Could not create DB")
	}

	err = databaseservice.GetInstance().CreateDB("trades")
	if err != nil {
		logrus.Error("Could not create DB")
	}

	err = databaseservice.GetInstance().CreateDB("telegram-chats")
	if err != nil {
		logrus.Error("Could not create DB")
	}
}
