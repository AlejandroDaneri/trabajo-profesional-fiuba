/* Import Libs */
import { useEffect, useState } from "react"
import { useDispatch } from "react-redux"
import styled from "styled-components"

/* Import WebApi */
import { list, start, stop } from "../webapi/strategy"

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
import View from "../components/reusables/View"
import FlotantBox, {
  FlotantBoxProvider,
} from "../components/reusables/FlotantBox"
import FieldSelect from "../components/reusables/FieldSelect"
import Strategy from "./Strategy"

const Strategies = () => {
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

  const [addModal, addModalFunc] = useState({
    show: false,
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
      default: true,
    },
    {
      value: "initial_balance",
      label: "Initial Balance",
    },
    {
      value: "balance",
      label: "Balance",
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

  const onStartStrategy = (strategyId) => {
    start(strategyId)
      .then((_) => {
        dispatch({
          type: POPUP_ACTION_OPEN,
          payload: {
            type: POPUP_TYPE_SUCCESS,
            message: "Strategy start Success",
          },
        })
        list_()
      })
      .catch((_) => {
        dispatch({
          type: POPUP_ACTION_OPEN,
          payload: {
            type: POPUP_TYPE_ERROR,
            message: "Could not start Strategy",
          },
        })
      })
  }

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

  const onToggleAddModal = () => {
    addModalFunc((prevState) => ({
      ...prevState,
      show: !prevState.show,
    }))
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
      row.current_balance,
      <div className="indicators">
        <FlotantBoxProvider>
          {row.indicators.map((indicator) => (
            <>
              <FlotantBox
                button={
                  <div className="indicator-button">{indicator.name}</div>
                }
                content={
                  <div className="indicator-content">
                    <div className="indicator">
                      <div className="parameters">
                        {Object.keys(indicator.parameters).map((parameter) => (
                          <div className="parameter">
                            <>{parameter}: </>
                            <>{indicator.parameters[parameter]}</>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                }
              />
            </>
          ))}
        </FlotantBoxProvider>
      </div>,
      <div className="currencies">
        {row.currencies.map((currency) => (
          <div className="currency">
            <CurrencyLogo currency={currency} />
          </div>
        ))}
      </div>,
      <div className="actions">
        {row.state === "created" && (
          <Button text="Start" onClick={() => onStartStrategy(row.id)} />
        )}
        {row.state === "running" && (
          <Button text="Stop" onClick={() => onStopStrategy(row.id)} />
        )}
        <Button text="Trades" onClick={() => onShowTrades(row.id)} />
      </div>,
    ]
  }

  const onAdd = () => {
    list_()
  }

  return (
    <>
      <Modal
        title="Trades"
        content={<Trades strategyID={tradesModal.data?.strategyID} />}
        open={tradesModal.show}
        onToggleOpen={onShowTrades}
      />
      <Modal
        title="Strategy"
        content={<Strategy onCloseModal={onToggleAddModal} onAdd={onAdd} />}
        open={addModal.show}
        onToggleOpen={onToggleAddModal}
        width="900px"
      />
      <View
        title="Strategies"
        buttons={[
          {
            icon: <i className="material-icons">add_circle</i>,
            label: "Add",
            onClick: onToggleAddModal,
          },
        ]}
        content={
          <StrategiesStyle>
            <Table headers={headers} data={state.data} buildRow={buildRow} />
          </StrategiesStyle>
        }
      />
    </>
  )
}

export default Strategies
