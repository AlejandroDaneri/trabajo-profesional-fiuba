/* Import Libs */
import { useEffect, useState } from "react"
import styled from "styled-components"

/* Import Components */
import Button from "../../Button"
import CurrencyLogo from "../../CurrencyLogo"

/* Import Reusables Components */
import FieldSelect from "../../reusables/FieldSelect"
import FieldSwitch from "../../reusables/FieldSwitch"
import FieldInput from "../../reusables/FieldInput"

/* Import Constants */
import { TIMEFRAMES } from "../../../constants"

/* Import WebApi */
import { add } from "../../../webapi/strategy"
import { list as listExchanges } from "../../../webapi/exchanges"
import { getIndicators as listIndicators } from "../../../webapi/backtesting"

/* Import Utils */
import { theme } from "../../../utils/theme"
import { capitalize } from "../../../utils/string"

const StrategyStyle = styled.div`
  display: flex;
  flex-direction: column;
  padding: 20px;

  & .section {
    display: flex;
    flex-direction: column;

    & .section-content.row {
      display: flex;
      flex-direction: row;
    }

    & .field {
      margin-right: 20px;
    }

    & h3 {
      border-bottom: 0.5px solid white;
      padding-bottom: 5px;
      margin-bottom: 10px;
    }
  }

  & .indicators {
    height: 300px;
    overflow-y: scroll;

    &::-webkit-scrollbar {
      -webkit-appearance: none;
      width: 8px;
    }

    &::-webkit-scrollbar-thumb {
      border-radius: 10px;
      background-color: ${theme.white};
    }
  }

  & .field {
    margin-bottom: 20px;
  }

  & .actions {
    display: flex;
    justify-content: end;
    margin-top: 20px;
    margin-bottom: 20px;

    & .cancel {
      margin-right: 10px;
    }
  }
`

const OptionStyle = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 60px;
  max-height: 20px;

  & p {
    margin: 0;
    color: ${theme.black};
  }

  & img {
    width: 20px;
    height: 20px;
  }
`

const Currency = ({ currency }) => {
  return (
    <OptionStyle>
      <p>{currency}</p>
      <CurrencyLogo currency={currency} />
    </OptionStyle>
  )
}

const CURRENCIES = ["BTC", "ETH", "SOL"]

const Strategy = ({ onCloseModal, onAdd }) => {
  const [strategy, strategyFunc] = useState({
    loading: false,
    data: {
      indicators: {}
    },
  })

  const [exchanges, exchangesFunc] = useState()

  const [indicators, indicatorsFunc] = useState({
    loading: false,
    data: []
  })

  const getExchanges = () => {
    listExchanges()
      .then((response) => {
        exchangesFunc(
          response.data.map((exchange) => ({
            value: exchange.id,
            label: exchange.alias,
          }))
        )
      })
      .catch(_ => {})
  }

  const getIndicators = () => {
    listIndicators()
      .then(response => {
        const indicators = response.data.reduce((indicators, indicator) => {
          return {
            ...indicators,
            [indicator.name]: {
              enabled: false,
              name: indicator.name,
              parameters: Object.keys(indicator.parameters).reduce(
                (parameters, parameter) => {
                  return {
                    ...parameters,
                    [parameter]: {
                      type: indicator.parameters[parameter].type,
                      value:
                        indicator.parameters[parameter].default === "required"
                          ? ""
                          : indicator.parameters[parameter].default,
                    },
                  }
                },
                {}
              ),
            },
          }
        }, {})
        indicatorsFunc({
          loading: false,
          data: indicators
        })
      })
      .catch(_ => {})
  }

  useEffect(() => {
    getExchanges()
    getIndicators()
  }, [])

  const onChange = (key, value) => {
    strategyFunc((prevState) => ({
      ...prevState,
      data: {
        ...prevState.data,
        [key]: value,
      },
    }))
  }

  const onChangeIndicatorEnabled = (key, value) => {
    const indicator = key.split(".")[0]

    strategyFunc((prevState) => ({
      ...prevState,
      data: {
        ...prevState.data,
        indicators: {
          ...prevState.data.indicators,
          [indicator]: {
            ...prevState.data.indicators[indicator],
            enabled: value,
          },
        },
      }
    }))
  }

  const onChangeIndicatorParameter = () => {}

  const transformToSend = (data) => {
    const createParameters = (indicator) => {
      // to-do: able to set this parameters in the ui
      switch (indicator) {
        case "RSI":
          return { buy_threshold: 30, rounds: 14, sell_threshold: 71 }
        case "MACD":
          return { slow: 26, fast: 12, smoothed: 20 }
        case "EMA":
          return { rounds: 100 }
        default:
          return {}
      }
    }

    return {
      currencies: strategy.data.currencies.map((row) => row.value),
      indicators: strategy.data.indicators.map((row) => {
        return {
          name: row.value,
          parameters: createParameters(row.value),
        }
      }),
      timeframe: strategy.data.timeframe.value,
      exchange_id: strategy.data.exchange?.value,
    }
  }

  const onSave = () => {
    strategyFunc((prevState) => ({
      ...prevState,
      loading: true,
    }))

    add(transformToSend(strategy.data))
      .then((_) => {
        strategyFunc((prevState) => ({
          ...prevState,
          loading: false,
        }))
        onCloseModal()
        onAdd()
      })
      .catch((_) => {
        strategyFunc((prevState) => ({
          ...prevState,
          loading: false,
        }))
      })
  }

  return (
    <StrategyStyle>
      <div className="section">
        <h3>Basic</h3>
        <div className="section-content row">
          <div className="field">
            <FieldSelect
              name="currencies"
              label="Currencies"
              value={strategy.currencies}
              onChange={onChange}
              options={CURRENCIES.map((currency) => ({
                value: currency,
                label: <Currency currency={currency} />,
              }))}
              width={200}
              multiple
            />
          </div>
          <div className="field">
            <FieldSelect
              name="timeframe"
              label="Timeframe"
              value={strategy.timeframe}
              onChange={onChange}
              options={TIMEFRAMES}
              width={200}
            />
          </div>
          <div className="field">
            <FieldSelect
              name="exchange"
              label="Exchange"
              value={strategy.exchange}
              onChange={onChange}
              options={exchanges}
              width={200}
            />
          </div>
        </div>
      </div>
      <div className="section">
        <h3>Indicators</h3>
        <div className="section-content">
          <div className="indicators">
            {Object.keys(indicators.data).map((indicator) => (
              <div className="section-content-row">
                <div className="field">
                  <FieldSwitch
                    name={indicator}
                    label={indicator}
                    value={strategy.data.indicators[indicator]?.enabled}
                    onChange={onChangeIndicatorEnabled}
                  />
                </div>
                {strategy.data.indicators[indicator]?.enabled && (
                  <>
                    {Object.keys(
                      indicators.data[indicator].parameters
                    ).map((parameter) => (
                      <div className="field">
                        <FieldInput
                          name={`${indicator}.${parameter}`}
                          label={parameter.split("_").map((word) => capitalize(word)).join(" ")}
                          value={strategy.data.indicators[indicator].parameters[parameter].value}
                          onChange={onChangeIndicatorParameter}
                        />
                      </div>
                    ))}
                  </>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
      
      
      <div className="actions">
        <div className="cancel">
          <Button text="Cancel" onClick={onCloseModal} />
        </div>
        <Button text="Save" onClick={onSave} loading={strategy.loading} />
      </div>
    </StrategyStyle>
  )
}

export default Strategy
