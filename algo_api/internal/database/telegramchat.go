package database

import "github.com/leesper/couchdb-golang"

type TelegramChat struct {
	PvtType string `json:"pvt_type"`
	TelegramChatPublicFields
	couchdb.Document
}

type TelegramChatPublicFields struct {
	ChatId          int64      `json:"chat_id"`
}
