using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace Client
{
    public partial class MyClientControl : NetManager.Client.ClientControl
    {
        public MyClientControl()
        {
            InitializeComponent();
            Client.Stopped += Client_Stopped;
        }

        private void Client_Stopped(object sender, EventArgs e)
        {
            button1.Enabled = true;
            button1.Text = "Старт";
        }

        private void button1_Click(object sender, EventArgs e)
        {
            if (Client.IsRunning)
            {
                button1.Enabled = false;
                Client.StopClient();
            }
            else
            {
                button1.Text = "Стоп";
                Client.StartClient();
            }
        }
    }
}
