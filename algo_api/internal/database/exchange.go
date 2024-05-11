package database

import "github.com/leesper/couchdb-golang"

type Exchange struct {
	PvtType string `json:"pvt_type"`
	ExchangePublicFields
	couchdb.Document
}

type ExchangePublicFields struct {
	Alias string `json:"alias"`
}

type ExchangeResponseFields struct {
	ExchangePublicFields
	ID string `json:"id"`
}
