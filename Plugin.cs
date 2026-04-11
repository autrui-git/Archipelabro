using System.Threading;
using BepInEx;
using BepInEx.Logging;
using UnityEngine;

namespace Archipelabro
{
    [BepInPlugin(MyPluginInfo.PLUGIN_GUID, MyPluginInfo.PLUGIN_NAME, MyPluginInfo.PLUGIN_VERSION)]
    public class Plugin : BaseUnityPlugin
    {
        internal static new ManualLogSource Logger;
        internal static Thread mThread;

        private void Awake()
        {
            // Plugin startup logic
            Logger = base.Logger;
            Logger.LogInfo($"Plugin {MyPluginInfo.PLUGIN_GUID} is loaded!");

            // Communication with client
            ThreadStart ts = new ThreadStart(CommunicationGameClient.GetInfo);
            mThread = new Thread(ts);
            mThread.Start();
        }
    }
}


