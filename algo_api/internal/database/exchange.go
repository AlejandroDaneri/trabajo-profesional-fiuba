package database

import "github.com/leesper/couchdb-golang"

type Exchange struct {
	PvtType string `json:"pvt_type"`
	ExchangePublicFields
	couchdb.Document
}

type ExchangePublicFields struct {
	Alias          string `json:"alias"`
	APISecret      string `json:"api_secret"`
	APIKey         string `json:"api_key"`
	TestingNetwork bool   `json:"testing_network"`
	ExchangeName   string `json:"exchange_name"`
}
type ExchangeResponseFields struct {
	ExchangePublicFields
	ID string `json:"id"`
}
