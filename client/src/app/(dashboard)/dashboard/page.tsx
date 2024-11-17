import Header from "../../../components/Nav/Nav";
import styles from "../../../styles/Dashboard.module.css";

// import { en } from '../../../../translations'; 

export default function Dashboard () {
    // const a = en
    return (
        <main className={styles.mainBackground}>
            <Header home={false} />
            <div className="container mt-4">
            <div className="row">
                <div className="col-md-4">
                    <div className="card">
                        <div className="card-header">Account Information</div>
                        <div className="card-body">
                            <p><strong>Balance:</strong> $<span id="accountBalance">0.00</span></p>
                            <p><strong>Equity:</strong> $<span id="accountEquity">0.00</span></p>
                            <p><strong>Free Margin:</strong> $<span id="freeMargin">0.00</span></p>
                        </div>
                    </div>
                </div>
                <div className="col-md-4">
                    <div className="card">
                        <div className="card-header">Trading Statistics</div>
                        <div className="card-body">
                            <p><strong>Total Trades:</strong> <span id="totalTrades">0</span></p>
                            <p><strong>Win Rate:</strong> <span id="winRate">0</span>%</p>
                            <p><strong>Profit Factor:</strong> <span id="profitFactor">0.00</span></p>
                        </div>
                    </div>
                </div>
                <div className="col-md-4">
                    <div className="card">
                        <div className="card-header">Current Position</div>
                        <div className="card-body">
                            <p><strong>Symbol:</strong> <span id="currentSymbol">EURUSD</span></p>
                            <p><strong>Type:</strong> <span id="positionType">-</span></p>
                            <p><strong>Profit/Loss:</strong> $<span id="currentPnL">0.00</span></p>
                        </div>
                    </div>
                </div>
            </div>

            <div className="row mt-4">
                <div className="col-md-8">
                    <div className="card">
                        <div className="card-header">Real-time Candlestick Chart</div>
                        <div className="card-body chart-container">
                            <div id="candlestickChart"></div>
                        </div>
                    </div>
                </div>
                <div className="col-md-4">
                    <div className="card">
                        <div className="card-header">Performance Chart</div>
                        <div className="card-body">
                            <canvas id="performanceChart"></canvas>
                        </div>
                    </div>
                </div>
            </div>

            <div className="row mt-4">
                <div className="col-md-6">
                    <div className="card">
                        <div className="card-header">Recent Trades</div>
                        <div className="card-body trade-log" id="tradeLog">
                            {/* Trade log entries will be dynamically added here */}
                        </div>
                    </div>
                </div>
                <div className="col-md-6">
                    <div className="card">
                        <div className="card-header">Latest News</div>
                        <div className="card-body" id="news">
                            {/* News articles will be dynamically added here */}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </main>
    )
}