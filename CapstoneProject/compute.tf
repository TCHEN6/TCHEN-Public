
#Create App Server
resource "aws_instance" "app_server" {
  #ami           = "ami-05fa00d4c63e32376"
  ami           = "ami-08c40ec9ead489470" #ubuntu
  instance_type = "t2.micro"
  key_name = "ec2_key"
  network_interface {
    device_index = 0
    network_interface_id = aws_network_interface.app_server_nic.id
  }
  tags = {
    Name = "App"
  }
    user_data = <<EOF
        #!/bin/bash
        echo "----------------------------SCRUMEATS SETUP START---------------------------------------------
        echo "download flask files..
        sudo curl https://pastebin.com/raw/UCm4QWYb >> app.py
        sudo curl https://pastebin.com/raw/74i7Cdc9 >> dynamodb_handler.py
        sudo add-apt-repository universe
        sudo apt update
        sudo apt-get install python3 
        sudo apt-get install python3-pip
        sudo pip3 install flask
        sudo pip3 install boto3
        sudo pip3 install python-decouple
        sudo python3 app.py
        echo "----------------------------SCRUMEATS SETUP END---------------------------------------------"
    EOF
}
#Create Bastion Box
resource "aws_instance" "bastion" {
  ami           = "ami-05fa00d4c63e32376" #AMAZON AMI
  #ami            = "ami-08c40ec9ead489470" #UBUNTU AMI
  instance_type = "t2.micro"
  #availability_zone = "us-east-1a"
  key_name = "ec2_key"
  network_interface {
    device_index = 0
    network_interface_id = aws_network_interface.bastion_nic.id
  }
  tags = {
    Name = "Bastion Box"
  }
    user_data = <<EOF
        #!/bin/bash
        echo "----------------------------SCRUMEATS SETUP START---------------------------------------------wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1Ssqq8nH8euiPF56rJyXP223lbCu9PKZW'
        echo "Running initial setup to prepare front end items"
        echo "Retrieve files..."
        sudo wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1c22VxrmPWJ3sReAMG2NsRaV_Wwd4ILQw' -O index.html
        sudo mv index.html /var/www/index.html
        #aws s3 cp index.html s3://scumlordsbucketpublic
        sudo yum  install httpd -y
        sudo systemctl start httpd
        echo "----------------------------SCRUMEATS SETUP END---------------------------------------------"
    EOF
}

#Create Web App Server (Used to be monitoring)
resource "aws_instance" "web_app_server" {
  ami = "ami-05fa00d4c63e32376"
  instance_type = "t2.micro"
  #availability_zone = "us-east-1a"
  key_name = "ec2_key" #Or Terraform_Key

  network_interface {
    device_index = 0
    network_interface_id = aws_network_interface.web_server_nic.id
  }

  user_data = <<-EOF
      #!/bin/bash
      sudo yum update -y
      sudo amazon-linux-extras install php8.0 mariadb10.5
      sudo yum install -y httpd
      sudo systemctl start httpd
      sudo systemctl enable httpd
      sudo usermod -a -G apache ec2-user
      sudo chown -R ec2-user:apache /var/www
      sudo chmod 2775 /var/www
      find /var/www -type d -exec sudo chmod 2775 {} \;
    EOF
    tags = {
      Name = "WebAppServer"
    }
}