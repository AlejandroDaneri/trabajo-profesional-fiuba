package telegramservice

import (
    "algo_api/internal/databaseservice"
    "sync"
    "fmt"
)

var instance IService
var once sync.Once

func GetInstance() IService {
    once.Do(func() {
        instance = NewService()
    })
    return instance
}

type TelegramService struct {
    databaseservice databaseservice.IService
}

func NewService() IService {
    return &TelegramService{
        databaseservice: databaseservice.GetInstance(),
    }
}

type IService interface {
    AddTelegramChat(chatId string) (error)
    GetAllTelegramChats() ([]string, error)
}

func (t *TelegramService) AddTelegramChat(chatId string) (error) {
    chat := make(map[string]interface{})
    dbName := "telegram-chats"
    db, err := t.databaseservice.GetDB(dbName)
    if err != nil {
        return err
    }
    chat["chat_id"] = chatId
    _, _, err = db.Save(chat, nil)
    if err != nil {
        return err
    }
    return nil
}

func (t *TelegramService) GetAllTelegramChats() ([]string, error) {
    dbName := "telegram-chats"
    db, err := t.databaseservice.GetDB(dbName)
    if err != nil {
        return nil, err
    }
    q := `
    {
        "selector": {
            "chat_id": {
                "$exists": true
            }
        }
    }
    `
    docs, err := db.QueryJSON(q)
    if err != nil {
        return nil, err
    }
    var chatIds []string
    for _, doc := range docs {
        chatId, ok := doc["chat_id"].(string)
        if !ok {
            return nil, fmt.Errorf("unexpected type for chat_id")
        }
        chatIds = append(chatIds, chatId)
    }
    return chatIds, nil
}

