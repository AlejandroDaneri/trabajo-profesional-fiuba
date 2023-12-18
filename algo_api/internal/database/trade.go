package database

import "github.com/leesper/couchdb-golang"

type Trade struct {
	PvtType string `json:"pvt_type"`
	TradePublicFields
	couchdb.Document
}

type TradePublicFields struct {
	Pair      string `json:"pair"`
	Price     string `json:"price"`
	Amount    string `json:"amount"`
	Timestamp int64  `json:"timestamp"`
	Type      string `json:"type"`
}

type TradeResponseFields struct {
	TradePublicFields
	ID string `json:"id"`
}
