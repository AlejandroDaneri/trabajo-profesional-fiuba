package database

import "github.com/leesper/couchdb-golang"

type Trade struct {
	PvtType string `json:"pvt_type"`
	TradePublicFields
	couchdb.Document
}

type TradePublicFields struct {
	Pair   string `json:"pair"`
	Amount string `json:"amount"`
	Orders struct {
		Buy struct {
			Price     string `json:"price"`
			Timestamp int64  `json:"timestamp"`
		} `json:"buy"`
		Sell struct {
			Price     string `json:"price"`
			Timestamp int64  `json:"timestamp"`
		} `json:"sell"`
	} `json:"orders"`
}

type TradeResponseFields struct {
	TradePublicFields
	ID string `json:"id"`
}
