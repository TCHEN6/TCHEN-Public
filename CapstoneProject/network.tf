resource "aws_internet_gateway" "var-gw" {
  vpc_id = aws_vpc.main.id
}
resource "aws_route_table" "igw-rt" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.var-gw.id
  }

  route {
    ipv6_cidr_block        = "::/0"
    gateway_id = aws_internet_gateway.var-gw.id
  }
  tags = {
    Name = "Internet Route"
  }
}
resource "aws_route_table_association" "route_table_assoc_public" {
  subnet_id      = aws_subnet.public-subnet.id
  route_table_id = aws_route_table.igw-rt.id
}
resource "aws_subnet" "public-subnet" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.0.0/25"
  tags = {
    Name = "Public Subnet"
  }
}
resource "aws_subnet" "private-subnet" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.1.0/25"
  tags = {
    Name = "Private Subnet"
  }
}
#EIP for Web App Server
resource "aws_eip" "eip1" {
  vpc                       = true
  network_interface         = aws_network_interface.web_server_nic.id
  associate_with_private_ip = "10.0.0.49"
  depends_on = [aws_internet_gateway.var-gw]
}
#NIC for Web App servier
resource "aws_network_interface" "web_server_nic" {
  subnet_id       = aws_subnet.public-subnet.id
  private_ips     = ["10.0.0.49"]
  security_groups = [aws_security_group.allow_web.id]
}
#NIC for Bastion instance
resource "aws_network_interface" "bastion_nic" {
  subnet_id       = aws_subnet.public-subnet.id
  private_ips     = ["10.0.0.50"]
  security_groups = [aws_security_group.allow_web.id]
}
#EIP for bastion instance
resource "aws_eip" "eip2" {
  vpc                       = true
  network_interface         = aws_network_interface.bastion_nic.id
  associate_with_private_ip = "10.0.0.50"
  depends_on = [aws_internet_gateway.var-gw]
}
#NIC for App instance
resource "aws_network_interface" "app_server_nic" {
  subnet_id       = aws_subnet.private-subnet.id
  private_ips     = ["10.0.1.51"]
  security_groups = [aws_security_group.flask_SG.id]
}
#EIP for App instance 
resource "aws_eip" "eip3" {
  vpc                       = true
  network_interface         = aws_network_interface.app_server_nic.id
  associate_with_private_ip = "10.0.1.51"
  depends_on = [aws_internet_gateway.var-gw]
}
resource "aws_nat_gateway" "private_nat_gw" {
  connectivity_type = "private"
  subnet_id         = aws_subnet.private-subnet.id

  tags = {
    name = "NAT for Private Subnet"
  }
}