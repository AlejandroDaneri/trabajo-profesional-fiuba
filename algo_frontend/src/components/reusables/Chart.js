import { CartesianGrid, Legend, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts"
import { theme } from "../../utils/theme"

const Chart = ({ data }) => {
    return (
        <ResponsiveContainer width="100%" height={400}>
            <LineChart
                data={data}
                margin={{
                    top: 5,
                    right: 30,
                    left: 20,
                    bottom: 5,
                }}
            >
                <CartesianGrid strokeDasharray="3 3" />
                <Tooltip />
                <Legend />

                <XAxis dataKey="date" />
                <YAxis label={{value: "Balance", position: "insideLeft"}} />

                <Line
                    type="monotone"
                    dataKey="balance"
                    name="Balance"
                    stroke={theme.btc}
                    activeDot={{ r: 8 }}
                    dot={false}
                />
            </LineChart>
        </ResponsiveContainer>
    )
}

export default Chart