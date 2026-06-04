"""
Full database seed script.

Usage:
    python seed_data.py

Creates 5 users + ~20 assets + ~80 inventory items +
~60 work orders + ~25 maintenance schedules.
Prints a credential table at the end.
"""

import asyncio
from datetime import datetime, timedelta, timezone

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings
from app.core.security import hash_password

# ─── Helpers ──────────────────────────────────────────────────────────────────

def utcnow() -> datetime:
    return datetime.now(timezone.utc)

def days(n: int) -> timedelta:
    return timedelta(days=n)

def oid() -> ObjectId:
    return ObjectId()

# ─── Seed data definitions ────────────────────────────────────────────────────

USERS = [
    {"full_name": "Ahmet Yılmaz",   "email": "admin@upkeep.com",        "password": "Admin1234",  "role": "admin"},
    {"full_name": "Mehmet Demir",   "email": "supervisor@upkeep.com",   "password": "Super1234",  "role": "supervisor"},
    {"full_name": "Fatma Kaya",     "email": "technician1@upkeep.com",  "password": "Tech1234!",  "role": "technician"},
    {"full_name": "Ali Çelik",      "email": "technician2@upkeep.com",  "password": "Tech5678!",  "role": "technician"},
    {"full_name": "Zeynep Arslan",  "email": "viewer@upkeep.com",       "password": "View1234!",  "role": "viewer"},
]

RAW_ASSETS = [
    # (tag, name, category, location)
    ("HVAC-001", "Central Air Conditioning Unit",   "HVAC",        "Building A – Rooftop"),
    ("HVAC-002", "Air Handling Unit #2",            "HVAC",        "Building B – Floor 3"),
    ("HVAC-003", "Rooftop Ventilation Fan",         "HVAC",        "Building A – Rooftop"),
    ("HVAC-004", "Chiller Unit",                    "HVAC",        "Basement – Plant Room"),
    ("ELEC-001", "Main Distribution Panel",         "Electrical",  "Basement – MV Room"),
    ("ELEC-002", "Emergency Generator",             "Electrical",  "Exterior – East Wing"),
    ("ELEC-003", "UPS System",                      "Electrical",  "Server Room"),
    ("ELEC-004", "Solar Inverter Array",            "Electrical",  "Rooftop"),
    ("PLMB-001", "Water Pumping Station",           "Plumbing",    "Basement – Utility"),
    ("PLMB-002", "Steam Boiler Unit",               "Plumbing",    "Basement – Boiler Room"),
    ("PLMB-003", "Cooling Tower",                   "Plumbing",    "Exterior – North Wing"),
    ("MECH-001", "Industrial Air Compressor",       "Mechanical",  "Production Hall – Bay 1"),
    ("MECH-002", "Conveyor Belt A",                 "Mechanical",  "Production Hall – Line 1"),
    ("MECH-003", "Conveyor Belt B",                 "Mechanical",  "Production Hall – Line 2"),
    ("MECH-004", "Hydraulic Press #1",              "Mechanical",  "Production Hall – Bay 2"),
    ("MECH-005", "CNC Lathe Machine",               "Mechanical",  "Workshop"),
    ("IT-001",   "Server Rack A",                   "IT",          "Server Room"),
    ("IT-002",   "Core Network Switch",             "IT",          "Server Room"),
    ("SAFE-001", "Fire Suppression System",         "Safety",      "Building-wide"),
    ("SAFE-002", "Emergency Lighting Grid",         "Safety",      "All Floors"),
]

RAW_INVENTORY = [
    # (sku, name, category, qty, threshold, unit_cost, unit, supplier, location)
    # Filters
    ("FLT-001", "HVAC Air Filter 20x20",        "Filters",             50, 10, 8.50,   "pcs", "FilterPro Ltd",    "Shelf A-1"),
    ("FLT-002", "HVAC Air Filter 24x24",        "Filters",             40, 10, 9.00,   "pcs", "FilterPro Ltd",    "Shelf A-1"),
    ("FLT-003", "Oil Filter (Generator)",       "Filters",             20,  5, 14.00,  "pcs", "GenParts Co",      "Shelf A-2"),
    ("FLT-004", "Hydraulic Return Filter",      "Filters",             15,  5, 22.50,  "pcs", "HydroSupply",      "Shelf A-3"),
    ("FLT-005", "Water Sediment Filter 10\"",   "Filters",             30,  8, 6.75,   "pcs", "WaterTech",        "Shelf A-2"),
    ("FLT-006", "Compressed Air Filter",        "Filters",             25,  5, 18.00,  "pcs", "CompressAir Inc",  "Shelf A-4"),
    # Bearings
    ("BRG-001", "Deep Groove Ball Bearing 6205","Bearings",            30,  6, 12.00,  "pcs", "SKF Distributor",  "Shelf B-1"),
    ("BRG-002", "Deep Groove Ball Bearing 6305","Bearings",            25,  5, 15.00,  "pcs", "SKF Distributor",  "Shelf B-1"),
    ("BRG-003", "Cylindrical Roller Bearing",   "Bearings",            20,  4, 28.00,  "pcs", "SKF Distributor",  "Shelf B-2"),
    ("BRG-004", "Thrust Ball Bearing 51206",    "Bearings",            15,  4, 19.50,  "pcs", "NSK Parts",        "Shelf B-2"),
    ("BRG-005", "Pillow Block Bearing UCP206",  "Bearings",            12,  3, 35.00,  "pcs", "NSK Parts",        "Shelf B-3"),
    # Lubricants
    ("LUB-001", "Mobil Grease XHP 222",         "Lubricants",         200, 30, 4.50,   "kg",  "Mobil Supplier",   "Cabinet L-1"),
    ("LUB-002", "Shell Tellus Oil 46",          "Lubricants",         150, 20, 6.00,   "litre","Shell Supplier",   "Cabinet L-2"),
    ("LUB-003", "Castrol Chain Lubricant",      "Lubricants",          80, 15, 8.00,   "litre","Castrol Dist.",    "Cabinet L-1"),
    ("LUB-004", "Compressor Oil ISO 100",       "Lubricants",         100, 20, 7.25,   "litre","TechOil Co",       "Cabinet L-3"),
    ("LUB-005", "Anti-Seize Compound 500g",     "Lubricants",          40,  8, 11.00,  "pcs", "ChemTech",         "Cabinet L-2"),
    # Electrical Components
    ("ELEC-101","MCB 16A Single Pole",          "Electrical Components",40, 8, 6.50,   "pcs", "ElecParts Store",  "Shelf E-1"),
    ("ELEC-102","MCB 32A Three Pole",           "Electrical Components",25, 5, 18.00,  "pcs", "ElecParts Store",  "Shelf E-1"),
    ("ELEC-103","Contactor 25A",                "Electrical Components",20, 4, 32.00,  "pcs", "Schneider Dist.",  "Shelf E-2"),
    ("ELEC-104","Thermal Relay 18-25A",         "Electrical Components",15, 3, 24.00,  "pcs", "Schneider Dist.",  "Shelf E-2"),
    ("ELEC-105","Control Cable 4x1.5mm 50m",   "Electrical Components",10, 2, 85.00,  "roll","CableTech",         "Rack E-3"),
    ("ELEC-106","Terminal Block 10mm²",         "Electrical Components",100,20, 1.20,   "pcs", "ElecParts Store",  "Shelf E-1"),
    ("ELEC-107","24V DC Power Supply 5A",       "Electrical Components",12, 3, 45.00,  "pcs", "MeanWell Dist.",   "Shelf E-3"),
    # Plumbing Parts
    ("PLMB-101","Gate Valve 1\" BSP",           "Plumbing Parts",      20, 4, 16.00,  "pcs", "ValvePro",         "Shelf P-1"),
    ("PLMB-102","Ball Valve 2\" BSP",           "Plumbing Parts",      15, 3, 28.00,  "pcs", "ValvePro",         "Shelf P-1"),
    ("PLMB-103","Pressure Gauge 0-10 bar",      "Plumbing Parts",      10, 3, 22.00,  "pcs", "Instrumentation Co","Shelf P-2"),
    ("PLMB-104","Flexible Hose 1/2\" x 500mm",  "Plumbing Parts",      25, 5, 9.50,   "pcs", "FlexPipe Ltd",     "Shelf P-2"),
    ("PLMB-105","Pump Impeller 80mm",           "Plumbing Parts",       8, 2, 95.00,  "pcs", "PumpParts Co",     "Shelf P-3"),
    ("PLMB-106","Check Valve 1.5\"",            "Plumbing Parts",      12, 3, 35.00,  "pcs", "ValvePro",         "Shelf P-1"),
    # Seals & Gaskets
    ("SEAL-001","O-Ring 50x3mm NBR",            "Seals & Gaskets",     100,20, 0.80,   "pcs", "SealTech",         "Bin S-1"),
    ("SEAL-002","O-Ring 80x4mm NBR",            "Seals & Gaskets",      80,15, 1.20,   "pcs", "SealTech",         "Bin S-1"),
    ("SEAL-003","Mechanical Seal Pump 35mm",    "Seals & Gaskets",      10, 2, 65.00,  "pcs", "SealPro",          "Bin S-2"),
    ("SEAL-004","Flange Gasket 4\" EPDM",       "Seals & Gaskets",      30, 5, 4.50,   "pcs", "GasketWorld",      "Bin S-2"),
    ("SEAL-005","PTFE Tape 12mm x 12m",         "Seals & Gaskets",     200,40, 0.60,   "pcs", "SealTech",         "Bin S-3"),
    ("SEAL-006","Shaft Seal 40x60x10mm",        "Seals & Gaskets",      15, 4, 18.00,  "pcs", "SealPro",          "Bin S-2"),
    # Fasteners
    ("FAST-001","Hex Bolt M10x50 (50pcs)",      "Fasteners",            30, 5, 4.00,   "pack","FastenerHub",      "Bin F-1"),
    ("FAST-002","Hex Bolt M12x60 (50pcs)",      "Fasteners",            25, 5, 5.50,   "pack","FastenerHub",      "Bin F-1"),
    ("FAST-003","Stainless Hex Nut M10 (100pcs)","Fasteners",           20, 4, 3.50,   "pack","FastenerHub",      "Bin F-2"),
    ("FAST-004","Spring Washer M10 (100pcs)",   "Fasteners",            20, 4, 2.00,   "pack","FastenerHub",      "Bin F-2"),
    ("FAST-005","Anchor Bolt M12x150",          "Fasteners",            40, 8, 1.80,   "pcs", "BuildFix",         "Bin F-3"),
    # Sensors & Instruments
    ("SENS-001","Temperature Sensor PT100",     "Sensors",              12, 3, 42.00,  "pcs", "SensorTech",       "Shelf I-1"),
    ("SENS-002","Pressure Transmitter 0-10 bar","Sensors",               8, 2, 115.00, "pcs", "SensorTech",       "Shelf I-1"),
    ("SENS-003","Flow Meter 2\" (DN50)",        "Sensors",               5, 1, 280.00, "pcs", "Instrumentation Co","Shelf I-2"),
    ("SENS-004","Vibration Sensor IEPE",        "Sensors",               6, 2, 160.00, "pcs", "SensorPro",        "Shelf I-2"),
    ("SENS-005","Proximity Switch NPN 12-24V",  "Sensors",              20, 5, 22.00,  "pcs", "AutoElec",         "Shelf I-1"),
    # Safety Equipment
    {"sku": "SAFE-101", "name": "Safety Gloves (L) 12-pack", "category": "Safety Equipment",
     "qty": 30, "threshold": 6, "unit_cost": 18.00, "unit": "pack",
     "supplier": "SafeWork Supply", "location": "Cabinet SF-1"},
    {"sku": "SAFE-102", "name": "Safety Goggles", "category": "Safety Equipment",
     "qty": 40, "threshold": 8, "unit_cost": 7.50, "unit": "pcs",
     "supplier": "SafeWork Supply", "location": "Cabinet SF-1"},
    {"sku": "SAFE-103", "name": "Hard Hat Class E", "category": "Safety Equipment",
     "qty": 20, "threshold": 4, "unit_cost": 24.00, "unit": "pcs",
     "supplier": "SafeWork Supply", "location": "Cabinet SF-2"},
    {"sku": "SAFE-104", "name": "Ear Protection 30dB (10-pack)", "category": "Safety Equipment",
     "qty": 25, "threshold": 5, "unit_cost": 12.00, "unit": "pack",
     "supplier": "SafeWork Supply", "location": "Cabinet SF-1"},
    # Cleaning & Consumables
    ("CONS-001","Isopropyl Alcohol 5L",         "Consumables",          20, 4, 16.00,  "bottle","ChemClean",      "Cabinet C-1"),
    ("CONS-002","Electrical Contact Cleaner",   "Consumables",          15, 3, 11.00,  "can", "ChemClean",        "Cabinet C-1"),
    ("CONS-003","Cable Ties 200mm (100pcs)",    "Consumables",          50,10, 3.50,   "pack","PackTech",         "Bin C-2"),
    ("CONS-004","Heat Shrink Tubing Assorted",  "Consumables",          30, 6, 6.00,   "pack","ElecParts Store",  "Bin C-2"),
    ("CONS-005","Duct Tape 50mm x 25m",         "Consumables",          20, 4, 5.50,   "roll","StickFix",         "Bin C-3"),
    ("CONS-006","WD-40 Lubricant 450ml",        "Consumables",          30, 6, 8.50,   "can", "ChemTech",         "Cabinet C-1"),
    ("CONS-007","Cleaning Rags 10kg",           "Consumables",          15, 3, 22.00,  "bag", "CleanPro",         "Cabinet C-3"),
    ("CONS-008","Silicone Sealant 310ml",       "Consumables",          20, 4, 9.00,   "tube","SealTech",         "Cabinet C-2"),
]

WO_TEMPLATES = [
    # (title, description, priority, status_index)
    # status_index → 0=open, 1=assigned, 2=in_progress, 3=completed, 4=closed
    ("HVAC Filter Replacement",         "Replace all air filters in Building A HVAC units",              "high",     3),
    ("Generator Monthly Inspection",    "Monthly check: fluid levels, battery, run test",                "high",     4),
    ("Conveyor Belt Tension Check",     "Check and adjust tension on Line 1 conveyor",                   "medium",   2),
    ("Boiler Safety Valve Test",        "Annual safety valve lift test and inspection",                  "critical", 3),
    ("UPS Battery Replacement",         "Replace 4x sealed lead-acid batteries in UPS unit",             "high",     1),
    ("Cooling Tower Cleaning",          "Descale and clean cooling tower fill media",                    "medium",   0),
    ("Compressor Belt Inspection",      "Inspect V-belts on industrial compressor, replace if worn",     "medium",   2),
    ("Fire Suppression Test",           "Annual system discharge test — coordinate with safety team",    "critical", 0),
    ("Server Room AC Service",          "Quarterly service of precision cooling unit in server room",    "high",     1),
    ("Hydraulic Press Oil Change",      "Drain and refill hydraulic fluid — 20L ISO VG 46",              "medium",   3),
    ("Chiller Leak Inspection",         "Inspect refrigerant lines for leaks — use electronic detector", "high",     2),
    ("Main Panel Thermography",         "Infrared scan of main distribution panel under load",           "high",     0),
    ("Pump Mechanical Seal Replacement","Replace worn mechanical seal on primary water pump",            "high",     3),
    ("CNC Lubrication Service",         "Clean and lubricate all CNC slide ways and ball screws",        "medium",   4),
    ("Emergency Lighting Battery Check","Test and log emergency light battery runtimes",                 "low",      1),
    ("Bearing Lubrication – Line 2",    "Grease all conveyor bearings on production Line 2",             "low",      2),
    ("Solar Inverter Log Review",       "Download and review 90-day performance logs",                   "low",      0),
    ("Ventilation Fan Balance Check",   "Check rooftop fan blade balance and vibration",                 "medium",   1),
    ("Water Filter Cartridge Swap",     "Replace sediment filter cartridges in the pump station",        "medium",   3),
    ("Boiler Flue Gas Analysis",        "Annual combustion efficiency test",                             "medium",   0),
    ("Network Switch Port Audit",       "Document active ports, update rack diagram",                    "low",      4),
    ("Security Camera Cleaning",        "Clean lenses, check alignment, verify recording",               "low",      0),
    ("Generator Load Bank Test",        "Full-load bank test to verify rated output capacity",           "high",     1),
    ("Pressure Gauge Calibration",      "Calibrate 12 pressure gauges against reference standard",       "medium",   2),
    ("Hydraulic Hose Inspection",       "Visual inspection of all high-pressure hoses for abrasion",     "high",     0),
    ("Air Compressor Valve Service",    "Disassemble and clean inlet/outlet valves",                     "medium",   3),
    ("Pump Station Level Sensor Check", "Test float switches and level transmitters",                    "low",      1),
    ("Electrical Panel Cleaning",       "Clean dust from all sub-panels — isolate before work",          "medium",   2),
    ("HVAC Coil Cleaning – Bldg B",    "High-pressure wash of evaporator and condenser coils",          "medium",   0),
    ("Lubrication Round – All Motors",  "Grease motor bearings plant-wide per lubrication chart",        "medium",   3),
    ("Control Panel Inspection",        "Check terminal tightness and label condition in all panels",    "low",      4),
    ("Boiler Water Treatment Check",    "Test water hardness, pH, TDS — add treatment chemicals",        "medium",   1),
    ("Overhead Crane Wire Rope Check",  "Visual and magnetic particle inspection of lifting wire",       "critical", 0),
    ("AHU Belt & Pulley Service",       "Replace drive belts and inspect pulleys on AHU #2",             "high",     2),
    ("Drain System Flushing",           "Flush all floor drains with bactericide solution",              "low",      0),
    ("Transformer Oil Sampling",        "Take DGA oil sample from main transformer",                     "high",     1),
    ("PLC Battery Replacement",         "Replace lithium backup batteries in all PLCs",                  "medium",   3),
    ("Vibration Analysis – Pumps",      "Collect vibration spectra from all rotating pumps",             "medium",   2),
    ("Roller Bearing Replacement",      "Replace failed bearings on Conveyor B tail pulley",             "high",     3),
    ("Insulation Resistance Test",      "Megger test on 400V motor cables",                              "medium",   0),
    ("Sprinkler Head Inspection",       "Visual inspection of all sprinkler heads for damage",           "medium",   1),
    ("Gas Detector Calibration",        "Bump test and span calibration of 8 gas detectors",             "high",     2),
    ("Hydraulic Cylinder Seal Kit",     "Replace seal kit on hydraulic press cylinder #2",               "high",     3),
    ("Chiller Condenser Tube Cleaning", "Brush clean condenser tubes to restore heat transfer",          "medium",   4),
    ("Electrical Earthing Test",        "Annual earth continuity and loop impedance testing",            "high",     0),
    ("Pump Coupling Alignment",         "Laser-align motor to pump coupling on station #2",              "medium",   1),
    ("HVAC Refrigerant Top-up",         "Check and top up refrigerant levels – R410A",                   "high",     2),
    ("Boiler Burner Service",           "Clean and set burner – check igniter and flame sensor",         "high",     3),
    ("Cooling Tower Fan Motor Service", "Check motor insulation, bearings and current draw",             "medium",   0),
    ("Annual Valve Exercise",           "Operate all isolation valves to prevent seizure",               "low",      4),
    ("Fire Door Inspection",            "Check all fire door seals, closers and release mechanisms",     "medium",   1),
    ("Hydraulic Fluid Contamination Test","Send hydraulic oil sample for particle count analysis",       "medium",   2),
    ("Control Room Panel Audit",        "Verify all indicators, alarms and annunciators are functional", "low",      0),
    ("Generator Fuel Tank Draining",    "Drain condensation from bottom of diesel tank",                 "low",      3),
    ("Compressor Intercooler Cleaning", "Remove and clean intercooler fins on air compressor",           "medium",   1),
    ("Safety Pressure Relief Valve Check","Lift-test all PRVs against set-point documentation",         "critical", 2),
    ("Electrical Panel IR Scan",        "Thermal imaging of all LV panels",                              "high",     0),
    ("Conveyor Belt Replacement",       "Replace worn belt section on Line 1 – 8m splice",               "high",     3),
    ("SCADA Historian Backup",          "Verify automated backup, test restore from last snapshot",      "low",      4),
    ("Motor Starter Inspection",        "Check contactors and overload relays in MCC",                   "medium",   0),
    ("Pump Impeller Clearance Check",   "Measure and adjust impeller wear ring clearance",               "medium",   1),
]

MAINT_TEMPLATES = [
    # (title, description, trigger_type, interval_days, usage_hours, priority)
    ("Monthly HVAC Filter Change",      "Replace air filters across all HVAC units",          "time_based", 30,  None,  "high"),
    ("Quarterly Generator Service",     "Full preventive service including oil and filters",  "time_based", 90,  None,  "high"),
    ("Annual Boiler Inspection",        "Full strip-down inspection and safety valve test",   "time_based", 365, None,  "critical"),
    ("Weekly Conveyor Inspection",      "Visual check of belt, rollers and guards",           "time_based", 7,   None,  "medium"),
    ("Bi-annual UPS Battery Test",      "Load test all UPS battery banks",                    "time_based", 180, None,  "high"),
    ("Compressor 500h Service",         "Oil, filter and valve service",                      "usage_based",None, 500,  "medium"),
    ("Monthly Pump Lubrication",        "Grease all pump motor bearings",                     "time_based", 30,  None,  "low"),
    ("Annual Electrical Thermography",  "IR scan of all distribution panels",                 "time_based", 365, None,  "high"),
    ("Quarterly Chiller Service",       "Clean coils, check refrigerant, test controls",      "time_based", 90,  None,  "high"),
    ("Monthly Fire System Test",        "Weekly detector test and monthly panel inspection",  "time_based", 30,  None,  "critical"),
    ("Annual Safety Valve Lift Test",   "Test all PRVs to verify set-point accuracy",         "time_based", 365, None,  "critical"),
    ("CNC 200h Lubrication",            "Full lubrication of all CNC axis slides",            "usage_based",None, 200,  "medium"),
    ("Monthly Cooling Tower Treatment", "Add biocide and descalant to cooling tower basin",   "time_based", 30,  None,  "medium"),
    ("Semi-annual Bearing Inspection",  "Vibration and temperature check on all critical motors","time_based",180,None,  "medium"),
    ("Weekly Emergency Light Test",     "Self-test function and log battery duration",         "time_based", 7,   None,  "low"),
    ("Hydraulic Press 1000h Service",   "Full fluid change and seal inspection",               "usage_based",None,1000,  "high"),
    ("Annual Gas Detector Calibration", "Full span calibration of all gas detectors",          "time_based", 365, None,  "high"),
    ("Monthly Lubrication Round",       "Scheduled lubrication of all plant rotating equipment","time_based",30,  None,  "low"),
    ("Quarterly Water Treatment Check", "Test boiler feed water and dosing system",            "time_based", 90,  None,  "medium"),
    ("Annual Earthing & Bonding Test",  "Earth loop impedance test on all LV circuits",        "time_based", 365, None,  "high"),
    ("Conveyor Belt 1000h Inspection",  "Full belt and idler roller replacement if worn",      "usage_based",None,1000,  "medium"),
    ("Bi-annual Valve Exercise",        "Operate all plant isolation valves",                  "time_based", 180, None,  "low"),
    ("Monthly CCTV Check",              "Clean lenses, verify recording on all cameras",       "time_based", 30,  None,  "low"),
    ("Transformer Oil Sampling",        "Annual dissolved gas analysis sample",                "time_based", 365, None,  "high"),
    ("Quarterly AHU Service",           "Belt, filter and coil service on all AHUs",           "time_based", 90,  None,  "high"),
]

# ─── Insert helpers ───────────────────────────────────────────────────────────

def make_user(u: dict) -> dict:
    now = utcnow()
    _id = oid()
    return {
        "_id": _id,
        "id": str(_id),
        "full_name": u["full_name"],
        "email": u["email"],
        "hashed_password": hash_password(u["password"]),
        "role": u["role"],
        "is_active": True,
        "department": None,
        "created_at": now,
        "updated_at": now,
    }

def make_asset(row: tuple, assigned_ids: list) -> dict:
    tag, name, category, location = row
    now = utcnow()
    _id = oid()
    import random
    return {
        "_id": _id,
        "id": str(_id),
        "name": name,
        "asset_tag": tag,
        "category": category,
        "status": random.choice(["active", "active", "active", "under_maintenance"]),
        "location": location,
        "assigned_to": str(random.choice(assigned_ids)),
        "purchase_date": (now - timedelta(days=random.randint(180, 1800))),
        "warranty_expires_at": (now + timedelta(days=random.randint(30, 730))),
        "repair_history": [],
        "model_number": f"MDL-{tag}",
        "serial_number": f"SN-{tag}-{random.randint(10000, 99999)}",
        "notes": "",
        "created_at": now,
        "updated_at": now,
    }

def make_inventory(row) -> dict:
    if isinstance(row, dict):
        sku, name, category = row["sku"], row["name"], row["category"]
        qty, threshold, unit_cost = row["qty"], row["threshold"], row["unit_cost"]
        unit, supplier, location = row["unit"], row["supplier"], row["location"]
    else:
        sku, name, category, qty, threshold, unit_cost, unit, supplier, location = row
    now = utcnow()
    _id = oid()
    return {
        "_id": _id,
        "id": str(_id),
        "name": name,
        "sku": sku,
        "category": category,
        "quantity_on_hand": qty,
        "low_stock_threshold": threshold,
        "unit_cost": unit_cost,
        "unit": unit,
        "supplier": supplier,
        "location": location,
        "consumption_log": [],
        "notes": "",
        "created_at": now,
        "updated_at": now,
    }

def make_work_order(tpl: tuple, asset_ids: list, user_ids: list, tech_ids: list) -> dict:
    import random
    title, description, priority, status_index = tpl
    statuses = ["open", "assigned", "in_progress", "completed", "closed"]
    status = statuses[min(status_index, 4)]

    now = utcnow()
    offset = random.randint(1, 60)
    created_at = now - timedelta(days=offset)
    _id = oid()

    doc = {
        "_id": _id,
        "id": str(_id),
        "title": title,
        "description": description,
        "status": status,
        "priority": priority,
        "asset_id": str(random.choice(asset_ids)),
        "assigned_to": str(random.choice(tech_ids)) if status != "open" else None,
        "created_by": str(random.choice(user_ids)),
        "due_date": created_at + timedelta(days=random.randint(3, 21)),
        "completed_at": (now - timedelta(days=random.randint(0, offset))) if status in ("completed", "closed") else None,
        "parts_used": [],
        "notes": "",
        "created_at": created_at,
        "updated_at": now,
    }
    return doc

def make_schedule(tpl: tuple, asset_ids: list, tech_ids: list) -> dict:
    import random
    title, description, trigger_type, interval_days, usage_hours, priority = tpl
    now = utcnow()
    _id = oid()

    last_triggered = now - timedelta(days=random.randint(0, interval_days or 60)) if interval_days else None
    next_due = (last_triggered + timedelta(days=interval_days)) if (last_triggered and interval_days) else (now + timedelta(days=random.randint(1, 30)))

    return {
        "_id": _id,
        "id": str(_id),
        "asset_id": str(random.choice(asset_ids)),
        "title": title,
        "description": description,
        "trigger_type": trigger_type,
        "interval_days": interval_days,
        "usage_threshold_hours": usage_hours,
        "current_usage_hours": (random.uniform(0, usage_hours * 0.9)) if usage_hours else None,
        "is_active": True,
        "last_triggered_at": last_triggered,
        "next_due_at": next_due,
        "generated_wo_priority": priority,
        "assigned_to": str(random.choice(tech_ids)),
        "created_at": now,
        "updated_at": now,
    }

# ─── Main ─────────────────────────────────────────────────────────────────────

async def seed() -> None:
    client = AsyncIOMotorClient(settings.mongo_uri)
    db = client[settings.db_name]

    print("Seeding database…\n")

    # ── Users ──────────────────────────────────────────────────────────────────
    user_docs = []
    for u in USERS:
        existing = await db["users"].find_one({"email": u["email"]})
        if existing:
            print(f"  [skip] user already exists: {u['email']}")
            user_docs.append(existing)
        else:
            doc = make_user(u)
            await db["users"].insert_one(doc)
            user_docs.append(doc)
    print(f"  [+] users: {len(user_docs)}")

    user_ids  = [d["_id"] for d in user_docs]
    tech_ids  = [d["_id"] for d in user_docs if d["role"] == "technician"]

    # ── Assets ─────────────────────────────────────────────────────────────────
    asset_docs = []
    for row in RAW_ASSETS:
        tag = row[0]
        existing = await db["assets"].find_one({"asset_tag": tag})
        if existing:
            asset_docs.append(existing)
        else:
            doc = make_asset(row, tech_ids)
            await db["assets"].insert_one(doc)
            asset_docs.append(doc)
    print(f"  [+] assets: {len(asset_docs)}")

    asset_ids = [d["_id"] for d in asset_docs]

    # ── Inventory ──────────────────────────────────────────────────────────────
    inv_docs = []
    for row in RAW_INVENTORY:
        sku = row["sku"] if isinstance(row, dict) else row[0]
        existing = await db["inventory_items"].find_one({"sku": sku})
        if existing:
            inv_docs.append(existing)
        else:
            doc = make_inventory(row)
            await db["inventory_items"].insert_one(doc)
            inv_docs.append(doc)
    print(f"  [+] inventory items: {len(inv_docs)}")

    # ── Work Orders ────────────────────────────────────────────────────────────
    wo_count = 0
    for tpl in WO_TEMPLATES:
        title = tpl[0]
        existing = await db["work_orders"].find_one({"title": title})
        if not existing:
            doc = make_work_order(tpl, asset_ids, user_ids, tech_ids)
            await db["work_orders"].insert_one(doc)
            wo_count += 1
    print(f"  [+] work orders: {wo_count}")

    # ── Maintenance Schedules ──────────────────────────────────────────────────
    sched_count = 0
    for tpl in MAINT_TEMPLATES:
        title = tpl[0]
        existing = await db["maintenance_schedules"].find_one({"title": title})
        if not existing:
            doc = make_schedule(tpl, asset_ids, tech_ids)
            await db["maintenance_schedules"].insert_one(doc)
            sched_count += 1
    print(f"  [+] maintenance schedules: {sched_count}")

    client.close()

    # ── Credentials summary ────────────────────────────────────────────────────
    print()
    print("=" * 60)
    print("  SEED COMPLETE — User Credentials")
    print("=" * 60)
    col_w = [20, 30, 14, 12]
    header = f"  {'Name':<{col_w[0]}} {'Email':<{col_w[1]}} {'Password':<{col_w[2]}} {'Role':<{col_w[3]}}"
    print(header)
    print("  " + "-" * (sum(col_w) + 3 * len(col_w)))
    for u in USERS:
        line = (
            f"  {u['full_name']:<{col_w[0]}} "
            f"{u['email']:<{col_w[1]}} "
            f"{u['password']:<{col_w[2]}} "
            f"{u['role']:<{col_w[3]}}"
        )
        print(line)
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(seed())
