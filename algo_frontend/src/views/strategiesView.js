/* Import Libs */
import { useEffect, useState } from "react"
import { useDispatch } from "react-redux"

import styled from "styled-components"

/* Import WebApi */
import { list, stop } from "../webapi/strategy"

/* Import Styles */
import StrategiesStyle from "../styles/strategies"

/* Import Utils */
import { capitalize } from "../utils/string"

/* Import Components */
import CurrencyLogo from "../components/CurrencyLogo"
import Table from "../components/Table"
import Button from "../components/Button"
import Trades from "../components/Trades"
import {
  POPUP_ACTION_OPEN,
  POPUP_TYPE_ERROR,
  POPUP_TYPE_SUCCESS,
} from "../components/Popup"
import Modal from "../components/reusables/Modal"

const ModalStyle = styled.div`
  display: flex;
  justify-content: center;
  border: 1px solid white;
  background: #282c34;
`

const StrategiesView = () => {
  const dispatch = useDispatch()

  const [state, stateFunc] = useState({
    loading: false,
    data: [],
  })

  const [tradesModal, tradesModalFunc] = useState({
    show: false,
    data: {
      strategyID: "",
    },
  })

  const transformToView = (data) => {
    return data.map((strategy) => ({
      ...strategy,
      state_label: capitalize(strategy.state),
    }))
  }

  const list_ = () => {
    list()
      .then((response) => {
        stateFunc({
          loading: false,
          data: transformToView(response?.data || []),
        })
      })
      .catch((_) => {
        stateFunc({
          loading: false,
        })
      })
  }

  useEffect(() => {
    list_()
  }, []) // eslint-disable-line

  const headers = [
    {
      value: "state",
      label: "State",
    },
    {
      value: "initial_balance",
      label: "Initial Balance",
    },
    {
      value: "indicators",
      label: "Indicators",
    },
    {
      value: "currencies",
      label: "Currencies",
    },
    {
      value: "actions",
      label: "Actions",
    },
  ]

  const onStopStrategy = (strategyId) => {
    stop(strategyId)
      .then((_) => {
        dispatch({
          type: POPUP_ACTION_OPEN,
          payload: {
            type: POPUP_TYPE_SUCCESS,
            message: "Strategy Stop Success",
          },
        })
        list_()
      })
      .catch((_) => {
        dispatch({
          type: POPUP_ACTION_OPEN,
          payload: {
            type: POPUP_TYPE_ERROR,
            message: "Could not stop Strategy",
          },
        })
      })
  }

  const onShowTrades = (strategyID) => {
    tradesModalFunc((prevState) => ({
      show: !prevState.show,
      data: {
        strategyID,
      },
    }))
  }

  const buildRow = (row) => {
    return [
      capitalize(row.state),
      row.initial_balance,
      <div className="indicators">
        {row.indicators.map((indicator) => (
          <div className="indicator">{indicator.name}</div>
        ))}
      </div>,
      <div className="currencies">
        {row.currencies.map((currency) => (
          <div className="currency">
            <CurrencyLogo currency={currency} />
          </div>
        ))}
      </div>,
      <div className="actions">
        {row.state === "running" && (
          <Button text="Stop" onClick={() => onStopStrategy(row.id)} />
        )}
        <Button text="Trades" onClick={() => onShowTrades(row.id)} />
      </div>,
    ]
  }

  return (
    <>
      <Modal
        title="Trades"
        content={<Trades strategyID={tradesModal.data?.strategyID} />}
        open={tradesModal.show}
        onToggleOpen={onShowTrades}
      />
      <StrategiesStyle>
        <div className="header">
          <h1>Strategies</h1>
        </div>
        <div className="content">
          <div className="strategies">
            <Table headers={headers} data={state.data} buildRow={buildRow} />
          </div>
        </div>
      </StrategiesStyle>
    </>
  )
}

export default StrategiesView
