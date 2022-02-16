from src.ec2.vpc import VPC

from src.client_locator import EC2Client


def main():
    # Create a VPC
    ec2_client = EC2Client().get_client()
    vpc = VPC(ec2_client)

    vpc_response = vpc.create_vpc()

    print('VPC created:' + str(vpc_response))

    # Add name tag to VPC
    vpc_name = 'Boto3-VPC'
    vpc_id = vpc_response['Vpc']['VpcId']
    vpc.add_name_tag(vpc_id, vpc_name)

    print('Added' + vpc_name + vpc_id)

    # Create Internet Gateway
    igw_response = vpc.create_internet_gateway_way()

    igw_id = igw_response['InternetGateway']['InternetGatewayId']

    vpc.attach_igw_to_vpc(vpc_id, igw_id)

    # Create a public subnet
    public_subnet_response = vpc.create_subnet(vpc_id, '10.0.1.0/24')

    public_subnet_id = public_subnet_response['Subnet']['SubnetId']

    print('Subnet created for VPC ' + vpc_id + ':' + str(public_subnet_response))

    # Add name tag tag to public subnet
    vpc.add_name_tag(public_subnet_id, 'Boto3-Public-Subnet')

    # Create Public Route Table
    public_route_table_response = vpc.create_public_route_table(vpc_id)

    rtb_id = public_route_table_response['RouteTable']['RouteTableId']

    #Adding the IGW to public route table
    vpc.create_igw_route_to_public_route_table(rtb_id, igw_id)

    # Associate Subnet with Route Table
    vpc.associate_subnet_with_route_table(public_subnet_id, rtb_id)

    # Allow auto-asign public ip addresses for subnet
    vpc.allow_auto_assign_ip_addresses_for_subnet(public_subnet_id)

    # Create a Private Subnet
    private_subnet_response = vpc.create_subnet(vpc_id, '10.0.2.0/24')
    private_subnet_id = private_subnet_response['Subnet']['SubnetId']

    print('Created private subnet ' + private_subnet_id + ' for VPC' + vpc_id)

    # Add name tag tag to private subnet
    vpc.add_name_tag(private_subnet_id, 'Boto3-Private-Subnet')


if __name__ == '__main__':
    main()
