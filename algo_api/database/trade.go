package database

import "github.com/leesper/couchdb-golang"

type Trade struct {
	PvtType string `json:"pvt_type"`
	TradePublicFields
	couchdb.Document
}

type TradePublicFields struct {
	Pair          string `json:"pair"`
	Prize         string `json:"prize"`
	Amount        string `json:"amount"`
	OpenTimestamp int64  `json:"open_timestamp"`
}
