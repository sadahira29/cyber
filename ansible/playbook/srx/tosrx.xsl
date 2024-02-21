<?xml version="1.0" encoding="utf-8" ?>
<xsl:transform version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="text" encoding="utf-8"/>

  <xsl:template match="/configuration">
    <xsl:text>---&#10;</xsl:text>
    <xsl:apply-templates />
  </xsl:template>
  
  <xsl:template match="system/login/user|system/syslog/user/contents|system/syslog/file|system/syslog/file/contents|system/ntp/server">
    <xsl:call-template name="loopnode"/>
  </xsl:template>

  <xsl:template match="interfaces/interface|interfaces/interface/unit|interfaces/interface/unit/family|interfaces/interface/unit/family/ethernet_switching/vlan/members|interfaces/interface/unit/family/inet/address|interfaces/interface/unit/family/inet/address/vrrp_group|interfaces/interface_range/member">
    <xsl:call-template name="loopnode"/>
  </xsl:template>

  <xsl:template match="snmp/trap_group/targets">
    <xsl:call-template name="loopnode"/>
  </xsl:template>

  <xsl:template match="routing_options/static/route">
    <xsl:call-template name="loopnode"/>
  </xsl:template>

  <xsl:template match="protocols/ospf/area/interface">
    <xsl:call-template name="loopnode"/>
  </xsl:template>

  <xsl:template match="security/policies/policy|security/zones/security_zone|security/zones/security_zone/host_inbound_traffic/system_services|security/zones/security_zone/host_inbound_traffic/protocols|security/nat/source/pool|security/nat/source/rule_set|security/policies/policy/policy|security/zones/security_zone/address_book/address|security/zones/security_zone/interfaces/host_inbound_traffic/system_services|security/policies/policy/policy/match/application|security/policies/policy/policy/match/source_address|security/zones/security_zone/interfaces/host_inbound_traffic/protocols">
    <xsl:call-template name="loopnode"/>
  </xsl:template>

  <xsl:template match="vlans/vlan">
    <xsl:call-template name="loopnode"/>
  </xsl:template>

  <xsl:template match="applications/application">
    <xsl:call-template name="loopnode"/>
  </xsl:template>

  <xsl:template name="loopnode">
    <xsl:if test="../*[name()=name(current())][1]=current()">
      <xsl:call-template name="indent">
	<xsl:with-param name="num" select="count(ancestor::*)"/>
      </xsl:call-template>
      <xsl:value-of select="concat(name(),':&#10;')"/>
    </xsl:if>
    <xsl:for-each select="*">
      <xsl:choose>
	<xsl:when test="position()=1">
	  <xsl:apply-templates select="." mode="loop"/>
	</xsl:when>
	<xsl:otherwise>
	  <xsl:apply-templates select="."/>
	</xsl:otherwise>
      </xsl:choose>
    </xsl:for-each>
  </xsl:template>

  <xsl:template match="*">
    <xsl:call-template name="indent">
      <xsl:with-param name="num" select="count(ancestor::*)"/>
    </xsl:call-template>
    <xsl:call-template name="printnode"/>
  </xsl:template>

  <xsl:template match="*" mode="loop">
    <xsl:call-template name="indent">
      <xsl:with-param name="num" select="count(ancestor::*) - 1"/>
    </xsl:call-template>
    <xsl:text>- </xsl:text>
    <xsl:call-template name="printnode"/>
  </xsl:template>

  <xsl:template name="printnode">
    <xsl:choose>
      <xsl:when test="name()='keys'">
	<xsl:value-of select="concat('_keys: &quot;', ./text(),'&quot;&#10;')"/>
      </xsl:when>
      <xsl:when test="count(*)=0 and text()">
	<xsl:value-of select="concat(name(),': &quot;', ./text(),'&quot;&#10;')"/>
      </xsl:when>
      <xsl:otherwise>
	<xsl:value-of select="concat(name(),':&#10;')"/>
	<xsl:apply-templates />
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template name="indent">
    <xsl:param name="num"/>
    <xsl:if test="$num &gt; 1">
      <xsl:text>  </xsl:text>
      <xsl:call-template name="indent">
	<xsl:with-param name="num" select="$num - 1"/>
      </xsl:call-template>
    </xsl:if>
  </xsl:template>

  <xsl:template match="text()">
    <xsl:value-of select="normalize-space(.)"/>
  </xsl:template>
</xsl:transform>
