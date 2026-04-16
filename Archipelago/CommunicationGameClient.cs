using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;

namespace Archipelabro
{
    public static class CommunicationGameClient
    {
        public static string connectionIP = "127.0.0.1";
        public static int connectionPort = 25001;
        static IPAddress localAdd;
        static TcpListener listener;
        static TcpClient client;
        static NetworkStream nwStream;

        static bool running;

        public static List<string> sendRequestBuffer = new List<string> { };

        public static void GetInfo()
        {
            localAdd = IPAddress.Parse(connectionIP);
            listener = new TcpListener(IPAddress.Any, connectionPort);
            listener.Start();

            client = listener.AcceptTcpClient();

            nwStream = client.GetStream();

            running = true;
            while (running)
            {
                ReceiveData();
            }
            listener.Stop();
        }

        static void ReceiveData()
        {
            byte[] buffer = new byte[client.ReceiveBufferSize];

            //---receiving Data from the Host----
            int bytesRead = nwStream.Read(buffer, 0, client.ReceiveBufferSize);
            string dataReceived = Encoding.UTF8.GetString(buffer, 0, bytesRead);

            if (dataReceived != null)
            {
                //---Using received data---
                Plugin.Logger.LogInfo("received : " + dataReceived + " from client");

                switch (dataReceived)
                {
                    case "ping":
                        SendData("pong");
                        break;
                    case "do_DeathLink":
                        Plugin.deathLinkPendin = true;
                        SendData("DeathLink_noted");
                        break;
                    case "ask":
                        string sender = "nothing";
                        if (sendRequestBuffer.Count > 0)
                        {
                            sender = sendRequestBuffer[0];
                            sendRequestBuffer.Remove(sender);
                        }
                        SendData(sender);
                        break;
                    case "":
                        Plugin.Logger.LogInfo("This data is empty...");
                        SendData("empty");
                        break;
                    default:
                        Plugin.Logger.LogInfo("This data is not defined...");
                        SendData("not_defined");
                        break;

                }
            }
        }

        static void SendData(string data)
        {
            Plugin.Logger.LogInfo("send : " + data + " to client");
            byte[] myWriteBuffer = Encoding.ASCII.GetBytes(data);
            nwStream.Write(myWriteBuffer, 0, myWriteBuffer.Length);
        }
    }
}
