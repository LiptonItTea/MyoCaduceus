namespace Client
{
    partial class Form1
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
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(Form1));
            this.myClientControl1 = new Client.MyClientControl();
            this.SuspendLayout();
            // 
            // myClientControl1
            // 
            this.myClientControl1.IPServer = ((System.Net.IPAddress)(resources.GetObject("myClientControl1.IPServer")));
            this.myClientControl1.Location = new System.Drawing.Point(13, 13);
            this.myClientControl1.Margin = new System.Windows.Forms.Padding(5, 5, 5, 5);
            this.myClientControl1.Name = "myClientControl1";
            this.myClientControl1.Size = new System.Drawing.Size(232, 423);
            this.myClientControl1.TabIndex = 0;
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(266, 450);
            this.Controls.Add(this.myClientControl1);
            this.Name = "Form1";
            this.Text = "Form1";
            this.ResumeLayout(false);

        }

        #endregion

        private MyClientControl myClientControl1;
    }
}

