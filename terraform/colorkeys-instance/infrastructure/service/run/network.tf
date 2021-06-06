### VPC ###

resource "aws_vpc" "stage_colorkeys" {
  cidr_block  = "10.0.0.0/16"
  tags        = var.default_tags
}

resource "aws_subnet" "stage_colorkeys_public_0" {
  vpc_id      = "${aws_vpc.stage_colorkeys.id}"
  cidr_block  = "10.0.1.0/24"
  tags        = var.default_tags
}

resource "aws_subnet" "stage_colorkeys_public_1" {
  vpc_id      = "${aws_vpc.stage_colorkeys.id}"
  cidr_block  = "10.0.2.0/24"
  tags        = var.default_tags
}

resource "aws_route_table" "stage_colorkeys_public" {
  vpc_id  = "${aws_vpc.stage_colorkeys.id}"
  tags    = var.default_tags
}

resource "aws_route_table_association" "stage_colorkeys_public_0" {
  subnet_id = aws_subnet.stage_colorkeys_public_0.id
  route_table_id  = aws_route_table.stage_colorkeys_public.id
}

resource "aws_route_table_association" "stage_colorkeys_public_1" {
  subnet_id = aws_subnet.stage_colorkeys_public_1.id
  route_table_id  = aws_route_table.stage_colorkeys_public.id
}

resource "aws_internet_gateway" "stage_colorkeys_igw" {
  vpc_id  = "${aws_vpc.stage_colorkeys.id}"
  tags    = var.default_tags
}

resource "aws_route" "stage_colorkeys_public_igw" {
  route_table_id          = "${aws_route_table.stage_colorkeys_public.id}"
  destination_cidr_block  = "0.0.0.0/0"
  gateway_id              = "${aws_internet_gateway.stage_colorkeys_igw.id}"
}

resource "aws_security_group" "stage_colorkeys_https" {
  name    = "stage-colorkeys-https"
  vpc_id  = "${aws_vpc.stage_colorkeys.id}"
  tags        = var.default_tags

  ingress {
    from_port = 443
    to_port   = 443
    protocol  = "TCP"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port = 0
    to_port   = 0
    protocol  = -1
    cidr_blocks = ["0.0.0.0/0"]
  }
}
