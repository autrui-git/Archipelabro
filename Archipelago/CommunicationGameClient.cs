using System;
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

        static bool running;

        public static void GetInfo()
        {
            localAdd = IPAddress.Parse(connectionIP);
            listener = new TcpListener(IPAddress.Any, connectionPort);
            listener.Start();

            client = listener.AcceptTcpClient();

            running = true;
            while (running)
            {
                SendAndReceiveData();
            }
            listener.Stop();
        }

        static void SendAndReceiveData()
        {
            NetworkStream nwStream = client.GetStream();
            byte[] buffer = new byte[client.ReceiveBufferSize];

            //---receiving Data from the Host----
            int bytesRead = nwStream.Read(buffer, 0, client.ReceiveBufferSize);
            string dataReceived = Encoding.UTF8.GetString(buffer, 0, bytesRead);

            if (dataReceived != null)
            {
                //---Using received data---
                Plugin.Logger.LogInfo(dataReceived);

                //---Sending Data to Host----
                if (dataReceived == "ping")
                {
                    Plugin.Logger.LogInfo("pong");
                    byte[] myWriteBuffer = Encoding.ASCII.GetBytes("pong");
                    nwStream.Write(myWriteBuffer, 0, myWriteBuffer.Length);
                }
            }
        }
    }
}
