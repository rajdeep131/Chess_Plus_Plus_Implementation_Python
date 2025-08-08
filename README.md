# ♟️ Chess++

**Chess++** is a custom-built chess variant created by **Rajdeep Das**, introducing new rules, strategic depth, and the original **Catapult** piece — designed to enhance traditional chess while preserving its elegance.

This repository contains the full implementation of Chess++ in Python, including:
- Full rule logic for all standard and new pieces
- Support for teleportation via Catapults
- Castling restrictions based on teleportation threats
- Custom Catapult capture rules
- Modular code design for expansion or GUI integration

---

## 🔮 What’s New in Chess++?

- 🧠 **Catapult Piece**: A non-capturing piece that allows allied pieces to teleport between two board locations.
- 🎯 **Teleportation Mechanics**: Add unpredictable and tactical possibilities — including teleporting into check.
- 🏰 **Castling Restrictions**: Castling is illegal if the opponent can teleport into your castling path.
- 💥 **Double Catapult Capture Rule**: Catapults can only be captured together when both are locked down.

Read the full rules in [`Chess++_Rules_Only.pdf`](./Chess++_Rules_Only.pdf).

---

## 🚀 How to Run

```bash
# Clone the repo
git clone https://github.com/your-username/chessplusplus.git
cd chessplusplus

# Run the main board setup (example usage)
python3 ChessPlusPlusBoard.py
