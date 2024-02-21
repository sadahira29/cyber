<?xml version="1.0" encoding="utf-8" ?>
<xsl:transform version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="xml" encoding="utf-8" indent="yes"/>

  <xsl:template match="/HP_config">
    <configuration>
      <system>
        <xsl:apply-templates select="hostname|dos-filter|no|max-vlans|time|fastboot|loop-protect|password|no"/>
	<xsl:if test="sntp">
	  <sntp><xsl:apply-templates select="sntp"/></sntp>
	</xsl:if>
      </system>
      <interfaces>
        <xsl:apply-templates select="interface"/>
      </interfaces>
      <snmp>
	<xsl:apply-templates select="snmp-server"/>
      </snmp>
      <routing_options>
        <static>
          <xsl:apply-templates select="ip"/>
	</static>
      </routing_options>
      <vlans>
        <xsl:apply-templates select="vlan|management-vlan"/>
      </vlans>
      <spanning_trees>
        <xsl:apply-templates select="spanning-tree"/>
      </spanning_trees>
    </configuration>
  </xsl:template>

  <xsl:template match="/*/hostname">
    <host_name><xsl:apply-templates select="value"/></host_name>
  </xsl:template>

  <xsl:template match="/*/max-vlans">
    <max_vlans><xsl:apply-templates select="value"/></max_vlans>
  </xsl:template>

  <xsl:template match="/*/management-vlan">
    <management_vlan><xsl:apply-templates select="value"/></management_vlan>
  </xsl:template>

  <xsl:template match="/*/sntp">
    <xsl:if test="server">
      <server>
	<priority><xsl:apply-templates select="value[1]"/></priority>
	<name><xsl:apply-templates select="value[2]"/></name>
      </server>
    </xsl:if>
  </xsl:template>

  <xsl:template match="/*/time">
    <xsl:if test="timezone">
      <time_zone><xsl:apply-templates select="value"/></time_zone>
    </xsl:if>
  </xsl:template>
  
  <xsl:template match="/*/ip">
    <xsl:if test="route">
      <route>
	<name>
	  <xsl:value-of select="value[1]"/>
	  <xsl:call-template name="masksize">
	    <xsl:with-param name="mask" select="value[2]"/>
	  </xsl:call-template>
	</name>
        <next_hop><xsl:apply-templates select="value[3]"/></next_hop>
      </route>
    </xsl:if>
  </xsl:template>

  <xsl:template match="/*/interface">
    <interface>
      <name><xsl:apply-templates select="value"/></name>
      <description><xsl:apply-templates select="name/value"/></description>
      <xsl:apply-templates select="*[name()!='value' and name()!='name']"/>
    </interface>
  </xsl:template>

  <xsl:template match="/*/snmp-server">
    <xsl:if test="community">
      <community>
	<name><xsl:apply-templates select="value"/></name>
	<xsl:apply-templates select="*[name()!='value' and name()!='community']"/>
      </community>
    </xsl:if>
    <xsl:if test="contact">
      <location><xsl:apply-templates select="value[2]"/></location>
      <contact><xsl:apply-templates select="value[1]"/></contact>
    </xsl:if>
  </xsl:template>

  <xsl:template match="/*/vlan">
    <vlan>
      <name><xsl:apply-templates select="name/value"/></name>
      <vlan_id><xsl:apply-templates select="value"/></vlan_id>
      <xsl:if test="tagged">
	<tagged><xsl:apply-templates select="tagged/value"/></tagged>
      </xsl:if>
      <xsl:if test="untagged">
	<untagged><xsl:apply-templates select="untagged/value"/></untagged>
      </xsl:if>
      <xsl:if test="no/untagged">
	<no_untagged><xsl:apply-templates select="no/value"/></no_untagged>
      </xsl:if>
      <xsl:if test="no/ip and no/address">
	<no_ip_address/>
      </xsl:if>
      <xsl:if test="ip/address">
        <ip_address>
	  <xsl:value-of select="ip/value[1]"/>
	  <xsl:call-template name="masksize">
	    <xsl:with-param name="mask" select="ip/value[2]"/>
	  </xsl:call-template>
	</ip_address>
      </xsl:if>
    </vlan>
  </xsl:template>

  <xsl:template name="masksize">
    <xsl:param name="mask"/>
    <xsl:choose>
      <xsl:when test="$mask='255.255.255.0'">
	<xsl:text>/24</xsl:text>
      </xsl:when>
      <xsl:when test="$mask='255.255.248.0'">
	<xsl:text>/21</xsl:text>
      </xsl:when>
      <xsl:otherwise>
	<xsl:text>/24</xsl:text>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template match="/*/spanning-tree">
    <spanning_tree>
      <name><xsl:apply-templates select="value"/></name>
      <xsl:apply-templates select="*[name()!='value']"/>
    </spanning_tree>
  </xsl:template>

  <xsl:template match="/*/loop-protect">
    <loop_protect>
      <disable_timer><xsl:apply-templates select="value"/></disable_timer>
    </loop_protect>    
  </xsl:template>

  <xsl:template match="/*/password">
    <xsl:if test="manager">
      <password_manager/>
    </xsl:if>
    <xsl:if test="operator">
      <password_operator/>
    </xsl:if>
  </xsl:template>

  <xsl:template match="/*/no">
    <xsl:if test="cdp and run">
      <no_cdp_run/>
    </xsl:if>
    <xsl:if test="cdp and enable">
      <no_cdp_enable><xsl:apply-templates select="value"/></no_cdp_enable>
    </xsl:if>
    <xsl:if test="tftp and server">
      <no_tftp_server/>
    </xsl:if>
    <xsl:if test="dhcp and config-file-update">
      <no_dhcp_config_file_update/>
    </xsl:if>
    <xsl:if test="dhcp and image-file-update">
      <no_dhcp_image_file_update/>
    </xsl:if>
  </xsl:template>

  <xsl:template match="*">
    <xsl:element name="{translate(name(), '-.', '_')}">
      <xsl:apply-templates />
    </xsl:element>
  </xsl:template>

  <xsl:template match="value|name">
    <xsl:value-of select="translate(text(),'&quot;','')"/>
  </xsl:template>

  <xsl:template match="text()">
    <xsl:value-of select="normalize-space(.)"/>
  </xsl:template>
</xsl:transform>
