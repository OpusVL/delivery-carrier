<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:output method="html" encoding="ISO-8859-1" />

	<xsl:variable name="UKDomSysId" select="'6'" />

	<xsl:param name="code39Barcode_url" select="CONSIGNMENTBATCH/BARCODEURL" />
	<xsl:param name="hostName" select="CONSIGNMENTBATCH/HOST" />
	<xsl:param name="images_dir" select="CONSIGNMENTBATCH/IMAGESDIR" />
	<xsl:param name="itemcount" select="0"></xsl:param>

	<xsl:template match="/">


		<html>
			<head>
				<title>TNT Label</title>

				<script type="text/javascript"><![CDATA[

					var firstPagePrinted = false;

					function includePageBreak() {

						if (firstPagePrinted) {
							document.writeln('<div class="pagebreak">');
							document.writeln('<font size="1" color="#FFFFFF">.</font>');
							document.writeln('</div>');
						} else {
							firstPagePrinted = true;
						}

					}

					]]>
				</script>
				<style><![CDATA[
							font.header { color : black; background-color : white; font-weight : bold; font-family : arial, helvetica "sans-serif"; font-size : 8pt; }


							 font.data { color : black; background-color : white; font-family : arial , "sans-serif"; font-size : 8pt; }

							 font.smallprint { color : black; background-color : white; font-family : arial, "sans-serif"; font-size : 6pt; }

							 div { page-break-after : always; }

							.data { }

							.dataBold { font-weight: bold; }

							.label { }

							 .deliveryDepot {  font-size: 96px;  }

							 .deliveryPostcode { font-size: xx-large; font-weight: bold; }

							 .normalService { font-size: x-large; }

								.premiumService { font-size: xx-large; font-weight: bold; }

					.tntTelephone { font-size: small; }

					.label {}


					]]>
				</style>
			</head>
			<body>

				<xsl:for-each select="CONSIGNMENTBATCH/CONSIGNMENT">
					<xsl:for-each select="PACKAGE">
					<xsl:variable name="packageitemcount" select="ITEMS"/>
					 <xsl:variable name="packageindex" select="PACKAGEINDEX"/>
					  <xsl:variable name="itemcount" select="PREVIOUSPACKAGEITEMCOUNT"/>
						 <xsl:call-template name="loop">
						    <xsl:with-param name="var" select="$packageitemcount"/>
						    <xsl:with-param name="itemcount">
						    <xsl:number value="number($itemcount)+1" />
	        				</xsl:with-param>
						  </xsl:call-template>
					</xsl:for-each>
				</xsl:for-each>
			</body>
		</html>
	</xsl:template>
	<xsl:template name="loop">
	  <xsl:param name="var"></xsl:param>
	  <xsl:param name="itemcount"></xsl:param>
	  <xsl:choose>
	    <xsl:when test="$var &gt; 0">
	      <xsl:choose>
							<xsl:when test="../@marketType='DOMESTIC'">
								<xsl:choose>
									<xsl:when test="../@originCountry='GB'">
										<xsl:call-template name="ukDomesticLabel">
											<xsl:with-param name="itemcount">
	    						<xsl:number value="number($itemcount)" />
	    					</xsl:with-param>
	    				</xsl:call-template>
									</xsl:when>
									<xsl:otherwise>
										<xsl:call-template name="internationalLabel">
											<xsl:with-param name="itemcount">
			    			<xsl:number value="number($itemcount)" />
	     				</xsl:with-param>
	     				</xsl:call-template>
									</xsl:otherwise>
								</xsl:choose>
							</xsl:when>
							<xsl:otherwise>
								<xsl:call-template name="internationalLabel">
				 	<xsl:with-param name="itemcount">
	    				<xsl:number value="number($itemcount)" />
					</xsl:with-param>
   				</xsl:call-template>
							</xsl:otherwise>
						</xsl:choose>
				<xsl:call-template name="loop">
	        <xsl:with-param name="var">
	        <xsl:number value="number($var)-1" />
	        </xsl:with-param>
	           <xsl:with-param name="itemcount">
			    <xsl:number value="number($itemcount)+1" />
	     		</xsl:with-param>
	      </xsl:call-template>
	    </xsl:when>
	    <xsl:otherwise>
	      <xsl:text></xsl:text>
	    </xsl:otherwise>
	  </xsl:choose>
	</xsl:template>

	<xsl:template name="defaultlLabel">
		<xsl:call-template name="internationalLabel" >
		<xsl:with-param name="itemcount">
	    				<xsl:number value="number($itemcount)" />
					</xsl:with-param>
		</xsl:call-template>
	</xsl:template>


	<xsl:template name="ukDomesticLabel">
		<xsl:param name="itemcount"></xsl:param>
		<xsl:variable name="collection-depot"
			select="format-number(../HEADER/COLLECTIONDEPOTNAME/@depotCode, '000')" />
		<xsl:variable name="delivery-depot"
			select="format-number(../DELIVERYDEPOTNAME/@depotCode, '000')" />

		<script type="text/Javascript">includePageBreak();</script>

		<table height="98%" cellpadding="0" cellspacing="0" border="0">
			<tr>
				<td>
					<table width="550" border="1" bordercolor="#000000"
						cellspacing="0" cellpadding="0">
						<tr>
							<xsl:choose>
								<xsl:when test="../SERVICE/@Premium='Y'">
									<td width="50%" align="center" class="premiumService">
										<xsl:value-of select="../SERVICESHORTNAME" />
									</td>
								</xsl:when>
								<xsl:otherwise>
									<td width="50%" align="center" class="normalService">
										<xsl:value-of select="../SERVICESHORTNAME" />
									</td>
								</xsl:otherwise>
							</xsl:choose>




							<td width="50%">
								<table width="100%" cellpadding="2" cellspacing="0">
									<tr>
										<td nowrap="nowrap" class="tntTelephone" align="center">
											Telephone
											<br class="" />
											�01827 303030
										</td>
										<td width="30%">
											<img src="{$hostName}{$images_dir}\tnt_logo.gif" width="167"
												height="83" border="0" />
										</td>
									</tr>
								</table>
							</td>
						</tr>
						<tr>
							<td valign="middle">
								<table width="100%" border="0" cellspacing="0"
									cellpadding="1">
									<tr>
										<td rowspan="6" width="1%">
											<img src="{$hostName}{$images_dir}\1x1.gif" width="1"
												height="1" />
										</td>
										<td class="label" width="45%">Coll. Depot:</td>
										<td width="64%">
											<span class="data">
												<xsl:value-of select="../HEADER/COLLECTIONDEPOTNAME" />
											</span>
											&#160;&#160;
											<span class="dataBold">
												<xsl:value-of select="../HEADER/COLLECTIONDEPOTNAME/@depotCode" />
											</span>
										</td>
									</tr>
									<tr>
										<td class="label">Sender A/c:</td>
										<td class="dataBold">
											<xsl:value-of
												select="format-number(../HEADER/SENDER/ACCOUNT , '0000000000')" />
										</td>
									</tr>
									<tr>
										<td class="label">Cons. No.</td>
										<td class="dataBold">
											<xsl:value-of select="substring(../CONNUMBER, 1, 8)" />
											<xsl:value-of select="substring(../CONNUMBER, 9, 1)" />
										</td>
									</tr>
									<tr>
										<td class="label">Weight (kg):</td>
										<td class="data">
											<xsl:value-of select="WEIGHT" />
										</td>
									</tr>
									<tr>
										<td>Item No.:</td>
										<td class="dataBold">
											<xsl:value-of select="format-number($itemcount,'000')" />
											of�
											<xsl:value-of select="format-number(../TOTALITEMS,'000')" />
										</td>
									</tr>
									<tr>
										<td class="label">Coll. Date :</td>
										<td class="data">
											<xsl:value-of select="../HEADER/SHIPMENTDATE" />
										</td>
									</tr>
								</table>
							</td>
							<td class="deliveryDepot" align="center" valign="middle">
								<xsl:value-of select="../DELIVERYDEPOTNAME/@depotCode" />
							</td>
						</tr>
						<tr>
							<td rowspan="3" valign="top">
								<table width="100%" border="0" cellspacing="1"
									cellpadding="1">
									<tr>
										<td rowspan="10" width="1%">
											<img src="{$hostName}{$images_dir}\1x1.gif" width="1"
												height="1" />
										</td>
										<td width="39%" class="label">Deliver to:</td>
									</tr>
									<xsl:choose>

										<xsl:when test="../DELIVERY/COMPANYNAME/text()">
											<tr>
												<td class="dataBold">
													<xsl:value-of select="../DELIVERY/CONTACTNAME" />
												</td>
											</tr>
											<tr>
												<td class="dataBold">
													<xsl:value-of select="../DELIVERY/COMPANYNAME" />
												</td>
											</tr>
											<tr>
												<td class="dataBold">
													<xsl:value-of select="../DELIVERY/STREETADDRESS1" />
												</td>
											</tr>
											<tr>
												<td class="dataBold">
													<xsl:value-of select="../DELIVERY/STREETADDRESS2" />
												</td>
											</tr>
											<tr>
												<td class="dataBold">
													<xsl:value-of select="../DELIVERY/STREETADDRESS3" />
												</td>
											</tr>
											<tr>
												<td class="dataBold">
													<xsl:value-of select="../DELIVERY/CITY" />
												</td>
											</tr>
											<tr>
												<td class="dataBold">
													<xsl:value-of select="../DELIVERY/PROVINCE" />
												</td>
											</tr>
											<tr>
												<td class="dataBold">
													<xsl:value-of select="../DELIVERY/POSTCODE" />
												</td>
											</tr>
											<tr>
												<td class="dataBold">
													<xsl:value-of select="../DELIVERY/COUNTRY" />
												</td>
											</tr>
										</xsl:when>
										<xsl:otherwise>
											<tr>
												<td class="dataBold">
													<xsl:value-of select="../RECEIVER/CONTACTNAME" />
												</td>
											</tr>
											<tr>
												<td class="dataBold">
													<xsl:value-of select="../RECEIVER/COMPANYNAME" />
												</td>
											</tr>
											<tr>
												<td class="dataBold">
													<xsl:value-of select="../RECEIVER/STREETADDRESS1" />
												</td>
											</tr>
											<tr>
												<td class="dataBold">
													<xsl:value-of select="../RECEIVER/STREETADDRESS2" />
												</td>
											</tr>
											<tr>
												<td class="dataBold">
													<xsl:value-of select="../RECEIVER/STREETADDRESS3" />
												</td>
											</tr>
											<tr>
												<td class="dataBold">
													<xsl:value-of select="../RECEIVER/CITY" />
												</td>
											</tr>
											<tr>
												<td class="dataBold">
													<xsl:value-of select="../RECEIVER/PROVINCE" />
												</td>
											</tr>
											<tr>
												<td class="dataBold">
													<xsl:value-of select="../RECEIVER/POSTCODE" />
												</td>
											</tr>
											<tr>
												<td class="dataBold">
													<xsl:value-of select="../RECEIVER/COUNTRY" />
												</td>
											</tr>
										</xsl:otherwise>
									</xsl:choose>
									<tr>
										<td height="10">
										</td>
									</tr>
								</table>
							</td>
							<td valign="top">
								<table width="100%" border="0" cellspacing="0"
									cellpadding="1">
									<tr>
										<td rowspan="2" width="1%">
											<img src="{$hostName}{$images_dir}\1x1.gif" width="1"
												height="1" />
										</td>
										<td class="label">Special Instructions:</td>
									</tr>
									<tr>
										<td class="dataBold">
											<xsl:value-of select="substring(../DELIVERYINST, 1, 25)" />
										</td>
									</tr>
								</table>
							</td>
						</tr>
						<tr>
							<td valign="top">
								<table width="100%" border="0" cellspacing="0"
									cellpadding="1">
									<tr>
										<td rowspan="2" width="1%">
											<img src="{$hostName}{$images_dir}\1x1.gif" width="1"
												height="1" />
										</td>
										<td class="label">Customer Reference:</td>
									</tr>
									<tr>
										<td class="dataBold">
											<xsl:value-of select="substring(../CUSTOMERREF, 1, 15)" />
										</td>
									</tr>
								</table>
							</td>
						</tr>
						<xsl:choose>

							<xsl:when test="../DELIVERY/COMPANYNAME/text()">
								<tr>
									<td align="center" class="deliveryPostcode">
										<xsl:value-of select="../DELIVERY/POSTCODE" />
									</td>
								</tr>
							</xsl:when>
							<xsl:otherwise>
								<tr>
									<td align="center" class="deliveryPostcode">
										<xsl:value-of select="../RECEIVER/POSTCODE" />
									</td>
								</tr>
							</xsl:otherwise>
						</xsl:choose>
						<tr>
							<td colspan="2" align="center" height="150" valign="middle">
								<xsl:value-of select="$UKDomSysId" />
								<xsl:value-of select="../HEADER/COLLECTIONDEPOTNAME/@depotCode" />
								<xsl:value-of
									select="format-number(../HEADER/SENDER/ACCOUNT, '0000000000')" />
								<xsl:value-of select="substring(../CONNUMBER, 1, 8)" />
								<xsl:value-of select="format-number(PACKAGEINDEX, '000')" />
								<xsl:value-of select="../DELIVERYDEPOTNAME/@depotCode" />
								<br />
								<img
									src="{$hostName}\barbecue?data={$UKDomSysId}{../HEADER/COLLECTIONDEPOTNAME/@depotCode}{format-number(../HEADER/SENDER/ACCOUNT, '0000000000')}{substring(../CONNUMBER, 1, 8)}{format-number(CONSIGNMENTBATCH/PACKAGE/PACKAGEINDEX, '000')}{../DELIVERYDEPOTNAME/@depotCode}&amp;type=UCC128&amp;appid=6&amp;height=105" />
							</td>
						</tr>
					</table>
				</td>
			</tr>
			<tr height="75%" valign="top" align="center">
				<td valign="center">
					<font size="20">
						<b>Address Label</b>
					</font>
					<br />
					<br />
					<br />
					<font class="data">Please fold this page and attach it to your parcel
					</font>
				</td>
			</tr>
		</table>
	</xsl:template>

	<xsl:template name="internationalLabel">
		<xsl:param name="itemcount"></xsl:param>
		<!--start of main table -->
		<table cellSpacing="0" width="600" border="1" height="500"
			cellPadding="3">
			<xsl:choose>
				<xsl:when test="../HEADER/COLLECTION/COMPANYNAME/text()">
					<tr>
						<td width="300" valign="top">
							<font class="header">Account :</font>
							<font class="data">
								<xsl:value-of select="../HEADER/SENDER/ACCOUNT" />
							</font>
							<br />
							<font class="header">Sender</font>
							<br />
							<font class="data">
								<xsl:value-of select="../HEADER/COLLECTION/COMPANYNAME" />
								<br />
								<xsl:value-of select="../HEADER/COLLECTION/STREETADDRESS1" />
								<br />
								<xsl:if test="../HEADER/COLLECTION/STREETADDRESS2/text()">
									<xsl:value-of select="../HEADER/COLLECTION/STREETADDRESS2" />
									<br />
								</xsl:if>
								<xsl:if test="../HEADER/COLLECTION/STREETADDRESS3/text()">
									<xsl:value-of select="../HEADER/COLLECTION/STREETADDRESS3" />
									<br />
								</xsl:if>
								<xsl:value-of select="../HEADER/COLLECTION/CITY" />
								<br />
								<xsl:if test="../HEADER/COLLECTION/PROVINCE/text()">
									<xsl:value-of select="../HEADER/COLLECTION/PROVINCE" />
									<br />
								</xsl:if>
								<xsl:if test="../HEADER/COLLECTION/POSTCODE/text()">
									<xsl:value-of select="../HEADER/COLLECTION/POSTCODE" />
									<br />
								</xsl:if>
								<xsl:value-of select="../HEADER/COLLECTION/COUNTRY" />
							</font>
							<br />
							<font class="header">Contact :</font>
							<font class="data">
								<xsl:value-of select="../HEADER/COLLECTION/CONTACTNAME" />
							</font>
							<br />
							<font class="header">Tel :</font>
							<font class="data">
								<xsl:value-of select="../HEADER/COLLECTION/CONTACTDIALCODE" />
								<xsl:value-of select="../HEADER/COLLECTION/CONTACTTELEPHONE" />
							</font>
						</td>
						<td align="center" width="300" colspan="2">
							<img src="{$hostName}{$images_dir}\logo.gif" />
							<br />
							<br />
							<img height="60" style="margin-right: 10px">
								<xsl:attribute name="src">
						         <xsl:value-of
									select="concat($hostName,concat($code39Barcode_url,../CONNUMBER))" />
						       </xsl:attribute>
							</img>
							<br />
							<font class="header">
								*
								<xsl:value-of select="/CONSIGNMENTBATCH/CONSIGNMENT/CONNUMBER" />
								*
							</font>
							<br />
							<br />
							<font class="header">Customer Reference :</font>
							<font class="data">
								<xsl:value-of select="../CUSTOMERREF" />
							</font>
						</td>
					</tr>
				</xsl:when>
				<xsl:otherwise>
					<tr>
						<td width="300" vAlign="top">
							<font class="header">Account :</font>
							<font class="data">
								<xsl:value-of select="../HEADER/SENDER/ACCOUNT" />
							</font>
							<br />
							<font class="header">Sender</font>
							<br />
							<font class="data">
								<xsl:value-of select="../HEADER/SENDER/COMPANYNAME" />
								<br />
								<xsl:value-of select="../HEADER/SENDER/STREETADDRESS1" />
								<br />
								<xsl:if test="../HEADER/SENDER/STREETADDRESS2/text()">
									<xsl:value-of select="../HEADER/SENDER/STREETADDRESS2" />
									<br />
								</xsl:if>
								<xsl:if test="../HEADER/SENDER/STREETADDRESS3/text()">
									<xsl:value-of select="../HEADER/SENDER/STREETADDRESS3" />
									<br />
								</xsl:if>
								<xsl:value-of select="../HEADER/SENDER/CITY" />
								<br />
								<xsl:if test="../HEADER/SENDER/PROVINCE/text()">
									<xsl:value-of select="../HEADER/SENDER/PROVINCE" />
									<br />
								</xsl:if>
								<xsl:if test="../HEADER/SENDER/POSTCODE/text()">
									<xsl:value-of select="../HEADER/SENDER/POSTCODE" />
									<br />
								</xsl:if>
								<xsl:value-of select="../HEADER/SENDER/COUNTRY" />
							</font>
							<br />
							<font class="header">Contact :</font>
							<font class="data">
								<xsl:value-of select="../HEADER/SENDER/CONTACTNAME" />
							</font>
							<br />
							<font class="header">Tel :</font>
							<font class="data">
								<xsl:value-of select="../HEADER/SENDER/CONTACTDIALCODE" />
								&#160;
								<xsl:value-of select="../HEADER/SENDER/CONTACTTELEPHONE" />
							</font>
						</td>
						<td align="center" width="300" colSpan="2">
							<img src="{$hostName}{$images_dir}\logo.gif" />
							<br />
							<br />
							<img height="60" style="margin-right: 10px">
								<xsl:attribute name="src">
						         <xsl:value-of
									select="concat($hostName,concat($code39Barcode_url,../CONNUMBER))" />
						       </xsl:attribute>
							</img>
							<br />
							<font class="header">
								*
								<xsl:value-of select="../CONNUMBER" />
								*
							</font>
							<br />
							<br />
							<font class="header">Customer Reference :</font>
							<font class="data">
								<xsl:value-of select="../CUSTOMERREF" />
							</font>
						</td>
					</tr>
				</xsl:otherwise>
			</xsl:choose>
			<xsl:choose>
				<xsl:when test="../DELIVERY/COMPANYNAME/text()">
					<tr>
						<td valign="top">
							<font class="header">Delivery Address</font>
							<br />
							<font class="data">
								<xsl:value-of select="../DELIVERY/COMPANYNAME" />
								<br />
								<xsl:value-of select="../DELIVERY/STREETADDRESS1" />
								<br />
								<xsl:if test="../DELIVERY/STREETADDRESS2/text()">
									<xsl:value-of select="../DELIVERY/STREETADDRESS2" />
									<br />
								</xsl:if>
								<xsl:if test="../DELIVERY/STREETADDRESS3/text()">
									<xsl:value-of select="../DELIVERY/STREETADDRESS3" />
									<br />
								</xsl:if>
								<xsl:value-of select="../DELIVERY/CITY" />
								<br />
								<xsl:if test="../DELIVERY/PROVINCE/text()">
									<xsl:value-of select="../DELIVERY/PROVINCE" />
									<br />
								</xsl:if>
								<xsl:if test="../DELIVERY/POSTCODE/text()">
									<xsl:value-of select="../DELIVERY/POSTCODE" />
									<br />
								</xsl:if>
								<xsl:value-of select="../DELIVERY/COUNTRY" />
							</font>
							<br />
							<font class="header">Contact :</font>
							<font class="data">
								<xsl:value-of select="../DELIVERY/CONTACTNAME" />
							</font>
							<br />
							<font class="header">Tel :</font>
							<font class="data">
								<xsl:value-of select="../DELIVERY/CONTACTDIALCODE" />
								<xsl:value-of select="../DELIVERY/CONTACTTELEPHONE" />
							</font>
						</td>

						<td colspan="2" valign="top">
							<font class="header">Shipment Date :</font>
							<font class="data">
								<xsl:value-of select="../HEADER/SHIPMENTDATE" />
							</font>
							<br />
							<font class="header">Description of Goods</font>
							<br />
							<font class="data">
								<xsl:value-of select="../GOODSDESC1" />
								<br />
								<xsl:value-of select="GOODSDESC" />
								<br />
								<br />
							</font>
							<font class="header">
								<br />
								Dimensions :
							</font>
							<xsl:if test="../CONSIGNMENTTYPE = 'N'">
								<font class="data">
									<xsl:value-of select="LENGTH" />
									<xsl:value-of select="LENGTH/@units" />
									x�
									<xsl:value-of select="WIDTH" />
									�
									<xsl:value-of select="WIDTH/@units" />
									�x�
									<xsl:value-of select="HEIGHT" />
									<xsl:value-of select="HEIGHT/@units" />
								</font>
							</xsl:if>
						</td>
					</tr>
				</xsl:when>
				<xsl:otherwise>
					<tr>
						<td vAlign="top">
							<font class="header">Delivery Address</font>
							<br />
							<font class="data">
								<xsl:value-of select="../RECEIVER/COMPANYNAME" />
								<br />
								<xsl:value-of select="../RECEIVER/STREETADDRESS1" />
								<br />
								<xsl:if test="../RECEIVER/STREETADDRESS2/text()">
									<xsl:value-of select="../RECEIVER/STREETADDRESS2" />
									<br />
								</xsl:if>
								<xsl:if test="../RECEIVER/STREETADDRESS3/text()">
									<xsl:value-of select="../RECEIVER/STREETADDRESS3" />
									<br />
								</xsl:if>
								<xsl:value-of select="../RECEIVER/CITY" />
								<br />
								<xsl:if test="../RECEIVER/PROVINCE/text()">
									<xsl:value-of select="../RECEIVER/PROVINCE" />
									<br />
								</xsl:if>
								<xsl:if test="../RECEIVER/POSTCODE/text()">
									<xsl:value-of select="../RECEIVER/POSTCODE" />
									<br />
								</xsl:if>
								<xsl:value-of select="../RECEIVER/COUNTRY" />
							</font>
							<br />
							<font class="header">Contact :</font>
							<font class="data">
								<xsl:value-of select="../RECEIVER/CONTACTNAME" />
							</font>
							<br />
							<font class="header">Tel :</font>
							<font class="data">
								<xsl:value-of select="../RECEIVER/CONTACTDIALCODE" />
								&#160;
								<xsl:value-of select="../RECEIVER/CONTACTTELEPHONE" />
							</font>
						</td>
						<td vAlign="top" colSpan="2">
							<font class="header">Shipment Date :</font>
							<font class="data">
								<xsl:value-of select="../HEADER/SHIPMENTDATE" />
							</font>
							<br />
							<font class="header">Description of Goods</font>
							<br />
							<font class="data">
								<xsl:value-of select="../GOODSDESC1" />
								<br />
								<xsl:value-of select="GOODSDESC" />
								<br />
								<br />
								<font class="header">Dimensions :</font>
								<xsl:if test="../CONSIGNMENTTYPE = 'N'">
									<font class="data">
										&#160;
										<xsl:value-of select="LENGTH" />
										&#160;
										<xsl:value-of select="LENGTH/@units" />
										&#160;x&#160;
										<xsl:value-of select="WIDTH" />
										&#160;
										<xsl:value-of select="WIDTH/@units" />
										&#160;x&#160;
										<xsl:value-of select="HEIGHT" />
										<xsl:value-of select="HEIGHT/@units" />
										&#160;
									</font>
								</xsl:if>
							</font>
						</td>
					</tr>
				</xsl:otherwise>
			</xsl:choose>
			<tr>
				<td colSpan="3">
					<font class="header">Special Delivery Instructions :</font>
					<font class="data">
						<xsl:value-of select="../DELIVERYINST" />
					</font>
				</td>
			</tr>
			<tr>
				<td>
					<font class="header">Service and Options</font>
					<br />
					<font class="data">
						<xsl:value-of select="../SERVICE" />
						<br />
						<xsl:value-of select="../OPTION1" />
						<br />
						<xsl:value-of select="../OPTION2" />
						<br />
						<xsl:value-of select="../OPTION3" />
						<br />
						<xsl:value-of select="../OPTION4" />
						<br />
						<xsl:value-of select="../OPTION5" />
					</font>
				</td>
				<td align="center" width="70">
					<font class="header">No of Items</font>
					<br />
					<font class="data">
						<xsl:value-of select="$itemcount" />
						of
						<xsl:value-of select="../TOTALITEMS" />
					</font>
					<br />
					<br />
					<font class="header">
						Item Weight
						<br />
					</font>
					<font class="data">
						<xsl:value-of select="WEIGHT" />
						&#160;
						<xsl:value-of select="WEIGHT/@units" />
					</font>
					<br />
				</td>
				<td>
					<font class="smallprint">TNT'S LIABILITY FOR LOSS, DAMAGE AND DELAY IS
						LIMITED BY THE CMR CONVENTION OR THE WARSAW CONVENTION WHICHEVER
						IS APPLICABLE. THE SENDER AGREES THAT THE GENERAL CONDITIONS,
						ACCESSIBLE AT
						HTTP://ICONNECTION.TNT.COM:81/TERMSANDCONDITIONS.HTML, ARE
						ACCEPTABLE AND GOVERN THIS CONTRACT. IF NO SERVICES OR BILLING
						OPTIONS ARE SELECTED THE FASTEST AVAILABLE SERVICE WILL BE CHARGED
						TO THE SENDER.</font>
				</td>
			</tr>
		</table>
		<xsl:choose>
			<xsl:when test="../HEADER/@last ='false'">
				<div>
					<font size="1" color="#5fffff">.</font>
				</div>
			</xsl:when>
			<xsl:otherwise>
				<xsl:if test="PACKAGEMAX != PACKAGEINDEX">
					<br />
					<br />
					<DIV>
						<FONT SIZE="1" COLOR="#5FFFFF">.</FONT>
					</DIV>
				</xsl:if>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
</xsl:stylesheet>
	<!--
		Stylus Studio meta-information - (c)1998-2003 Copyright Sonic Software
		Corporation. All rights reserved. <metaInformation> <scenarios
		><scenario default="no" name="UKDomesticLabel" userelativepaths="yes"
		externalpreview="no" url="..\label.xml" htmlbaseurl=""
		outputurl="newCombinedLabel.html" processortype="internal"
		commandline="" additionalpath="" additionalclasspath=""
		postprocessortype="none" postprocesscommandline=""
		postprocessadditionalpath="" postprocessgeneratedext=""/><scenario
		default="yes" name="CombinedLabel22" userelativepaths="yes"
		externalpreview="no" url="UKDOMESTIC&#x2D;LABEL.xml" htmlbaseurl=""
		outputurl="..\html\newCombinedLabel.html" processortype="msxml4"
		commandline="" additionalpath="" additionalclasspath=""
		postprocessortype="none" postprocesscommandline=""
		postprocessadditionalpath=""
		postprocessgeneratedext=""/></scenarios><MapperInfo srcSchemaPath=""
		srcSchemaRoot="" srcSchemaPathIsRelative="yes"
		srcSchemaInterpretAsXML="no" destSchemaPath="" destSchemaRoot=""
		destSchemaPathIsRelative="yes" destSchemaInterpretAsXML="no"/>
		</metaInformation>
	-->