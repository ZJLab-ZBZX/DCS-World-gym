-- Data export script for DCS, version 1.2.
-- Copyright (C) 2006-2014, Eagle Dynamics.
-- See http://www.lua.org for Lua script system info 
-- We recommend to use the LuaSocket addon (http://www.tecgraf.puc-rio.br/luasocket) 
-- to use standard network protocols in Lua scripts.
-- LuaSocket 2.0 files (*.dll and *.lua) are supplied in the Scripts/LuaSocket folder
-- and in the installation folder of the DCS. 
-- Expand the functionality of following functions for your external application needs.
-- Look into Saved Games\DCS\Logs\dcs.log for this script errors, please.
-- local Tacviewlfs = require('lfs')
-- dofile(lfs.writedir() .. [[Scripts\DCS-BIOS\BIOS.lua]])
-- dofile(lfs.writedir() .. 'Scripts/dataExport.lua')
-- ÃÂ¦ÃÂÃÂ¥ÃÂ¥ÃÂ¿ÃÂÃÂ¦ÃÂÃÂÃÂ¤ÃÂ»ÃÂ¶ÃÂ¨ÃÂ®ÃÂ¾ÃÂ§ÃÂ½ÃÂ®
-- local function logAllObjs(message)
--     local file = io.open(lfs.writedir() .. 'Logs/objsExport.log', "a")
--     file:write(os.date("[%Y-%m-%d %H:%M:%S] ") .. message .. "\n")
--     file.close()
-- end
-- local Tacviewlfs = require('lfs')
-- local json = dofile("Scripts/dkjson.lua")

-- local TacviewLuaExportStart = LuaExportStart
-- local TacviewLuaExportBeforeNextFrame = LuaExportBeforeNextFrame
-- local TacviewLuaExportAfterNextFrame = LuaExportAfterNextFrame
-- local TacviewLuaExportStop = LuaExportStop

function LuaExportStart()
    -- if TacviewLuaExportStart then
    --     TacviewLuaExportStart()
    -- end
    -- Works once just before mission start.
    -- Make initializations of your files or connections here.
    -- Socket
    package.path = package.path .. ";" .. lfs.currentdir() .. "/LuaSocket/?.lua"
    package.cpath = package.cpath .. ";" .. lfs.currentdir() .. "/LuaSocket/?.dll"
    socket = require("socket")
    host = "127.0.0.1" --"172.26.104.67"
    port1 = 10010 -- ÃÂ¥ÃÂÃÂÃÂ©ÃÂÃÂÃÂ¤ÃÂ¿ÃÂ¡ÃÂ¦ÃÂÃÂ¯ÃÂ§ÃÂ«ÃÂ¯

    logObjs = io.open(lfs.writedir() .. 'Logs/objsExport.log', "w")

    -- TCP setup
    c = assert(socket.tcp())
    c:connect(host, port1)
    c:setoption('keepalive', true)
    c:setoption('reuseaddr', true)
    c:settimeout(10)

    -- UDP setup
    -- -- send
    -- c = socket.udp()
    -- c:setpeername(host, port1)
    -- c:settimeout(10) -- set the timeout for reading the socket 

    -- -- receive
    -- port2 = 10021 -- ÃÂ¦ÃÂÃÂ¥ÃÂ¦ÃÂÃÂ¶ÃÂ¥ÃÂÃÂ½ÃÂ¤ÃÂ»ÃÂ¤ÃÂ§ÃÂ«ÃÂ¯
    -- d = socket.udp()
    -- d:setsockname('127.0.0.1', port2)
    -- d:settimeout(10) -- set the timeout for reading the socket
    -- å19æ­¥æ¯ä¸æ¬¡å¢å ä¸åï¼ä¹å°±æ¯å½19æ¶æ¯20åéï¼19å¾åÃ10åéä¹å°±æ¯ç¬¬20æ¬¡æ¶æ¶30åéï¼21æ¬¡æ¶æ¯40åé...
    local accelerate_time = 10
    for i = 1,accelerate_time-1 do
        LoSetCommand(53)
    end

    LoSetCommand(52)
    
    socket.try(c:send('game start'))
end

function LuaExportBeforeNextFrame()
    -- if TacviewLuaExportBeforeNextFrame then
    --     TacviewLuaExportBeforeNextFrame()
    -- end
    --ProcessInput()
end

function LuaExportAfterNextFrame()
    -- if TacviewLuaExportAfterNextFrame then
    --     TacviewLuaExportAfterNextFrame()
    -- end

    -- Works just after every simulation frame.
    -- Call Lo*() functions to get data from Lock On here.
    -- local t = LoGetModelTime()
    -- local selfData = LoGetSelfData()

    -- local IAS = LoGetIndicatedAirSpeed() -- (m/s)
    -- local TAS = LoGetTrueAirSpeed() -- (m/s)
    -- local altBar = LoGetAltitudeAboveSeaLevel() -- meters
    -- local altRad = LoGetAltitudeAboveGroundLevel() -- meters
    -- local AoA = LoGetAngleOfAttack() -- rad
    -- local AU = LoGetAccelerationUnits() -- table {x = Nx,y = NY,z = NZ} (G)
    -- local VV = LoGetVerticalVelocity() -- (m/s)
    -- local mach = LoGetMachNumber()
    -- local pitch, bank, yaw = LoGetADIPitchBankYaw() -- (rad)ÃÂ¥ÃÂ§ÃÂ¿ÃÂ¦ÃÂÃÂÃÂ¦ÃÂÃÂÃÂ¥ÃÂ¼ÃÂÃÂ¤ÃÂ»ÃÂª
    -- local MagY = LoGetMagneticYaw() -- (rad)
    -- local airPressure = LoGetBasicAtmospherePressure() -- (mm hg)
    -- local HSI = LoGetControlPanel_HSI()
    -- local Engine = LoGetEngineInfo()
    -- {
    --     RPM = {left, right},(%)
    --     Temperature = { left, right}, (Celcium degrees)
    --     HydraulicPressure = {left ,right},kg per square centimeter
    --     FuelConsumption   = {left ,right},kg per sec
    --     fuel_internal      -- fuel quantity internal tanks	kg
    --     fuel_external      -- fuel quantity external tanks	kg

    -- }
    -- if selfData then
    --     socket.try(c:send(string.format(
    --         "t = %.2f, name = %s, LatLongAlt = (%f, %f, %f), altBar = %.2f, alrRad = %.2f, pitch = %.2f, bank = %.2f, yaw = %.2f, heading =%.2f, IAS = %.2f, TAS = %.2f, AoA = %.2f, mach = %.2f",
    --         t, selfData.Name, selfData.LatLongAlt.Lat, selfData.LatLongAlt.Long, selfData.LatLongAlt.Alt, altRad,
    --         altBar, pitch, bank, yaw, selfData.Heading, IAS, TAS, AoA, mach)))
    -- else
    --     socket.try(c:send("self data not found."))
    -- end

    -- local o = LoGetWorldObjects("units")
    -- for k, v in pairs(o) do
    --     if v.Type.level1 == 1 then -- ÃÂ¨ÃÂ¿ÃÂÃÂ¦ÃÂ»ÃÂ¤ÃÂ¨ÃÂÃÂ·ÃÂ¥ÃÂÃÂÃÂ¦ÃÂÃÂÃÂ¦ÃÂÃÂÃÂ§ÃÂ©ÃÂºÃÂ¤ÃÂ¸ÃÂ­ÃÂ§ÃÂÃÂ®ÃÂ¦Ã ÃÂ
    --         allobjs = string.format(
    --             "t = %.2f, ID = %d, name = %s, country = %s(%s), LatLongAlt = (%f, %f, %f), heading = %f\n", t, k,
    --             v.Name, v.Country, v.Coalition, v.LatLongAlt.Lat, v.LatLongAlt.Long, v.LatLongAlt.Alt, v.Heading)
    --         logObjs:write(os.date("[%Y-%m-%d %H:%M:%S] ") .. allobjs .. "\n")
    --         -- socket.try(c:send("running..."))
    --     end
    -- end
end

function LuaExportActivityNextEvent(t)
    local tNext = t 
    local t = LoGetModelTime()
    local o = LoGetWorldObjects("units")
    local selfData = LoGetSelfData()
    local TAS = LoGetTrueAirSpeed()
    local pitch, bank, yaw = LoGetADIPitchBankYaw()
    local vel = LoGetVectorVelocity() -- vel.x: vel towards north, vel.y: vertical vel (upwards vel), vel.z: vel towards east
    local vela = LoGetAngularVelocity()

    -- local aircraft = Unit.getByName('target1')

    local trg = LoGetLockedTargetInformation()

    local message_string = string.format('{"system": {"time": %.2f}', t)

    if selfData then
        message_string = message_string .. string.format(',\n"self": {"name": "%s", "country": "%s(%s)", "LatLongAlt": [%f,%f,%f], "Attitude": [%f,%f,%f], "Velocity": [%f,%f,%f], "AngularVelocity": [%f,%f,%f], "Heading": %f, "TAS": %f}',
        selfData.Name, selfData.Country, selfData.Coalition, selfData.LatLongAlt.Lat, selfData.LatLongAlt.Long, selfData.LatLongAlt.Alt, bank, pitch, yaw, vel.x, vel.y, vel.z, vela.x, vela.y, vela.z, selfData.Heading,TAS)
    end
    
    for k,v in pairs(o) do
        message_string = message_string .. string.format(',\n"%d": {"name": "%s", "unit": "%s", "country": "%s(%s)", "LatLongAlt": [%f,%f,%f], "Attitude": [%f, %f, %f]}',
        k, v.Name, tostring(v.UnitName), v.Country, v.Coalition, v.LatLongAlt.Lat, v.LatLongAlt.Long, v.LatLongAlt.Alt, v.Bank, v.Pitch, v.Heading)
    end

    -- for i,cur in pairs(trg) do
    --     message_string = message_string .. string.format(",\nID = %d, position = (%f,%f,%f) , V = (%f,%f,%f),flags = 0x%x",cur.ID,cur.position.p.x,cur.position.p.y,cur.position.p.z,cur.velocity.x,cur.velocity.y,cur.velocity.z,cur.flags)
    -- end
  
    message_string = message_string .. '}\n\n'
    socket.try(c:send(message_string))
   
    tNext = tNext + 0.1
    ProcessInput()

    -- UDP setup
    -- while true do
    --     local ready = socket.select({d},nil, 1)
    --     if #ready > 0 then
    --         ProcessInput()
    --         break
    --     end
    -- end


    return tNext
end

function LuaExportStop()
    -- if TacviewLuaExportStop then
    --     TacviewLuaExportStop()
    -- end
    -- Works once just after mission stop.
    -- Close files and/or connections here.
    socket.try(c:send("quit")) -- to close the listener socket
    c:close()
    logObjs:close()

end

function ProcessInput()

    local data, err = c:receive()

    -- UDP setup
    -- local data, err = d:receive()
  
    if data then
        toTable = loadstring("return " .. data)
        command = toTable()

        for key, value in pairs(command) do
            
            if type(value) == "number" then
                LoSetCommand(key, value)
            elseif type(value) == "boolean" then
                LoSetCommand(key)
            end
            
        end
    end
end


local Tacviewlfs=require('lfs');dofile(Tacviewlfs.writedir()..'Scripts/TacviewGameExport.lua')
