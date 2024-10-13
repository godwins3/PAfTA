from flask import jsonify
from db.mongo_conn import create as create_mongo_conn
from bson import json_util
import json

def fetch_trade_logs(symbol="EURUSD"):
    try:
        # Initialize MongoDB connection
        client = create_mongo_conn()
        db = client['trades']  # Changed from 'exodus' to 'trades'
        collection = db[symbol]  # Use the symbol as the collection name

        # Fetch all trade logs
        trade_logs = list(collection.find())

        # Close MongoDB connection
        client.close()

        # Convert ObjectId to string for JSON serialization
        trade_logs = json.loads(json_util.dumps(trade_logs))

        return jsonify({
            'status': 'success',
            'data': trade_logs
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

def fetch_trade_logs_by_timeframe(start_time, end_time, symbol="EURUSD"):
    try:
        # Initialize MongoDB connection
        client = create_mongo_conn()
        db = client['trades']  # Changed from 'exodus' to 'trades'
        collection = db[symbol]  # Use the symbol as the collection name

        # Query trade logs within the given timeframe
        query = {
            'Trade_Open_Time': {
                '$gte': start_time,
                '$lte': end_time
            }
        }
        trade_logs = list(collection.find(query))

        # Close MongoDB connection
        client.close()

        # Convert ObjectId to string for JSON serialization
        trade_logs = json.loads(json_util.dumps(trade_logs))

        return jsonify({
            'status': 'success',
            'data': trade_logs
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
