"""Tiny disposable REST backend for the CRUD-chain test.

Public mock APIs (dummyjson.com, reqres.in, etc.) echo back a fake id on
POST but never actually store anything, so there's nothing honest to verify
on a follow-up GET. This gives the CRUD-chain test a real, in-memory store
instead — started fresh before the test session and thrown away after.
Not meant to resemble a production API; it's a fixture, not a product.
"""

from __future__ import annotations

import json
import threading
from pathlib import Path

from flask import Flask, jsonify, request
from werkzeug.serving import make_server

FIXTURE_FILE = Path(__file__).parent / "db.json"


def _load_seed() -> list[dict]:
    with open(FIXTURE_FILE, encoding="utf-8") as f:
        return json.load(f)["users"]


def create_app() -> Flask:
    app = Flask(__name__)
    state = {"users": _load_seed(), "next_id": 1000}

    @app.get("/users")
    def list_users():
        return jsonify(state["users"])

    @app.post("/users")
    def create_user():
        payload = request.get_json(force=True)
        new_id = state["next_id"]
        state["next_id"] += 1
        record = {"id": new_id, **payload}
        state["users"].append(record)
        return jsonify(record), 201

    @app.get("/users/<int:user_id>")
    def get_user(user_id: int):
        for user in state["users"]:
            if user["id"] == user_id:
                return jsonify(user)
        return jsonify({"error": f"user {user_id} not found"}), 404

    @app.patch("/users/<int:user_id>")
    def patch_user(user_id: int):
        payload = request.get_json(force=True)
        for user in state["users"]:
            if user["id"] == user_id:
                user.update(payload)
                return jsonify(user)
        return jsonify({"error": f"user {user_id} not found"}), 404

    @app.delete("/users/<int:user_id>")
    def delete_user(user_id: int):
        before = len(state["users"])
        state["users"] = [u for u in state["users"] if u["id"] != user_id]
        if len(state["users"]) == before:
            return jsonify({"error": f"user {user_id} not found"}), 404
        return jsonify({"deleted": user_id}), 200

    return app


class FixtureServerThread(threading.Thread):
    """Runs the Flask app on a background thread so pytest can start/stop
    it around the test session without shelling out to a separate process."""

    def __init__(self, port: int):
        super().__init__(daemon=True)
        self.server = make_server("127.0.0.1", port, create_app())

    def run(self):
        self.server.serve_forever()

    def stop(self):
        self.server.shutdown()
