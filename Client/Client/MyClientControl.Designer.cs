namespace Client
{
    partial class MyClientControl
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.button1 = new System.Windows.Forms.Button();
            this.pNetworkSettings.SuspendLayout();
            this.gbClients.SuspendLayout();
            this.SuspendLayout();
            // 
            // pNetworkSettings
            // 
            this.pNetworkSettings.Controls.Add(this.button1);
            this.pNetworkSettings.Controls.SetChildIndex(this.button1, 0);
            this.pNetworkSettings.Controls.SetChildIndex(this.lIP, 0);
            this.pNetworkSettings.Controls.SetChildIndex(this.lPort, 0);
            this.pNetworkSettings.Controls.SetChildIndex(this.tbIP, 0);
            this.pNetworkSettings.Controls.SetChildIndex(this.lClientName, 0);
            // 
            // chClients
            // 
            this.chClients.Size = new System.Drawing.Size(224, 106);
            // 
            // tbName
            // 
            this.tbName.Size = new System.Drawing.Size(99, 22);
            // 
            // button1
            // 
            this.button1.Location = new System.Drawing.Point(124, 86);
            this.button1.Name = "button1";
            this.button1.Size = new System.Drawing.Size(75, 23);
            this.button1.TabIndex = 19;
            this.button1.Text = "Старт";
            this.button1.UseVisualStyleBackColor = true;
            this.button1.Click += new System.EventHandler(this.button1_Click);
            // 
            // MyClientControl
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.Name = "MyClientControl";
            this.pNetworkSettings.ResumeLayout(false);
            this.pNetworkSettings.PerformLayout();
            this.gbClients.ResumeLayout(false);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Button button1;
    }
}
