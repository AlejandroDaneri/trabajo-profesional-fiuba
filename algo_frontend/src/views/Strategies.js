/* Import Libs */
import { useEffect, useState } from "react"
import { useDispatch } from "react-redux"
import BounceLoader from "react-spinners/BounceLoader"
import moment from 'moment'

/* Import WebApi */
import { list, remove, start, stop } from "../webapi/strategy"
import { get as getExchange } from "../webapi/exchanges"

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

/* Import Views */
import Strategy from "./Strategy"

/* Import Images */
import logoBinance from "../images/logos/exchanges/binance.svg"

/* Import Constants */
import { TIMEFRAMES } from "../constants"

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

    const transformState = (state) => {
      switch (state) {
        case 'created':
          return 0
        case 'running':
          return 1
        case 'finished':
          return 2
        default:
          return 0
      }
    }

    const getDuration = (start, end) => {
      const end_ = end || (Date.now() / 1000)
      return moment.utc((end_ - start) * 1000).format('HH:mm:ss')
    }

    const transformTimeframe = (timeframe) => {
      return TIMEFRAMES.find(timeframe_ => timeframe_.value === timeframe)?.label
    }

    return data.map((strategy) => ({
      ...strategy,
      state_value: transformState(strategy.state),
      state_label: capitalize(strategy.state),
      duration: getDuration(strategy.start_timestamp, strategy.end_timestamp),
      timeframe: transformTimeframe(strategy.timeframe),
      current_balance: parseInt(strategy.current_balance).toFixed(2)
    })).reduce((strategies, strategy) => {
      return {
        ...strategies,
        [strategy.id]: strategy
      }
    }, {})
  }

  const getStrategies = () => {
    return new Promise((resolve, reject) => {
      stateFunc(prevState => ({
        ...prevState,
        loading: true,
      }))
      list()
        .then((response) => {
          stateFunc({
            loading: false,
            data: transformToView(response?.data || []),
          })
          resolve(response.data)
        })
        .catch((_) => {
          stateFunc({
            loading: false,
          })
        })
    })
  }

  const getState = () => {
    getStrategies()
      .then(strategies => {
        strategies.forEach(strategy => {
          getExchange(strategy.exchange_id)
            .then(response => {
              stateFunc(prevState => ({
                ...prevState,
                data: {
                  ...prevState.data,
                  [strategy.id]: {
                    ...prevState.data[strategy.id],
                    exchange: response.data
                  }
                }
              }))
            })
            .catch(_ => {})
        })
      })
  }

  useEffect(() => {
    const interval = setInterval(getState, 10000)
    getState()

    return () => {
      clearInterval(interval)
    }
  }, []) // eslint-disable-line

  const headers = [
    {
      value: "state_value",
      label: "State",
      default: true,
      width: 10,
    },
    {
      value: "initial_balance",
      label: "Initial Balance",
      width: 10,
    },
    {
      value: "balance",
      label: "Balance",
      width: 10,
    },
    {
      value: "profit_and_loss",
      label: "Profit and Loss",
      width: 10,
    },
    {
      value: "timeframe",
      label: "Timeframe",
      width: 10,
    },
    {
      value: "duration",
      label: "Duration",
      width: 10,
    },
    {
      value: "exchange",
      label: "Exchange",
      width: 10,
    },
    {
      value: "indicators",
      label: "Indicators",
      width: 10,
    },
    {
      value: "currencies",
      label: "Currencies",
      width: 10,
    },
    {
      value: "actions",
      label: "Actions",
      width: 20,
    },
  ]

  const onRemoveStrategy = (strategyId) => {
    remove(strategyId)
      .then((_) => {
        dispatch({
          type: POPUP_ACTION_OPEN,
          payload: {
            type: POPUP_TYPE_SUCCESS,
            message: "Strategy remove Success",
          },
        })
        getStrategies()
      })
      .catch((_) => {
        dispatch({
          type: POPUP_ACTION_OPEN,
          payload: {
            type: POPUP_TYPE_ERROR,
            message: "Could not remove Strategy",
          },
        })
      })
  }

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
        getStrategies()
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
        getStrategies()
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
    const getPL = (row) => {
      const profitAndLoss = (row.current_balance - row.initial_balance).toFixed(2)
      const profitAndLossPercentaje = (
        (row.current_balance / row.initial_balance - 1) *
        100
      ).toFixed(2)
      return `${profitAndLoss} (${profitAndLossPercentaje}%)`
    }

    return [
      <div className="state">
        <p>{capitalize(row.state)}</p>
        {row.state === "running" && <div className="loader"><BounceLoader color="white" size={18} /></div>}
      </div>,
      row.initial_balance,
      row.current_balance,
      getPL(row),
      row.timeframe,
      row.duration,
      row.exchange === 'binance' && <img alt="Binance" src={logoBinance} width="24px" />,
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
          <div className="button-container">
            <Button
              width={25}
              height={25}
              text={<i className="material-icons">play_arrow</i>}
              onClick={() => onStartStrategy(row.id)}
              tooltip="Play"
              circle
            />
          </div>
        )}
        {row.state === "running" && (
          <div className="button-container">
            <Button
              width={25}
              height={25}
              text={<i className="material-icons">stop</i>}
              onClick={() => onStopStrategy(row.id)}
              tooltip="Stop"
              circle
            />
          </div>
        )}
        <div className="button-container">
          <Button
            width={25}
            height={25}
            text={<i className="material-icons">list</i>}
            onClick={() => onShowTrades(row.id)}
            tooltip="Trades"
            circle
          />
        </div>
        <div className="button-container">
          <Button
            width={25}
            height={25}
            text={<i className="material-icons">delete</i>}
            onClick={() => onRemoveStrategy(row.id)}
            tooltip="Delete"
            circle
          />
        </div>
      </div>,
    ]
  }

  const onAdd = () => {
    getStrategies()
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
        loading={state.loading}
        buttons={[
          {
            icon: <i className="material-icons">add_circle</i>,
            label: "Add",
            onClick: onToggleAddModal,
          },
        ]}
        content={
          <StrategiesStyle>
            <Table headers={headers} data={Object.values(state.data)} buildRow={buildRow} />
          </StrategiesStyle>
        }
      />
    </>
  )
}

export default Strategies
