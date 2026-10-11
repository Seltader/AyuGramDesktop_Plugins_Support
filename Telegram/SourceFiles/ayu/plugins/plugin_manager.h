// This is the source code of AyuGram for Desktop.
//
// We do not and cannot prevent the use of our code,
// but be respectful and credit the original author.
//
// Copyright @Radolyn, 2026
#pragma once

#include <QString>
#include <QVector>
#include <memory>
#include "ui/text/text_entity.h"

namespace AyuPlugins {

struct PluginInfo {
	QString id;
	QString name;
	QString description;
	QString author;
	QString version;
	bool enabled = false;
	QString error;
};

class PluginManager final {
public:
	static PluginManager &Instance();

	void init();
	void deinit();

	// Hook for outgoing messages (on_send_message_hook)
	// Returns false if message sending should be cancelled.
	bool onSendMessage(
		int account,
		QString &text,
		EntitiesInText &entities,
		uint64 replyToMsgId = 0);

	// Returns path to plugins directory (%APPDATA%/AyuGram/plugins)
	QString pluginsDir() const;

	// List discovered plugins
	QVector<PluginInfo> getInstalledPlugins();

	// Reload all plugins
	void reloadPlugins();

	// Enable/disable
	void setPluginEnabled(const QString &id, bool enabled);

private:
	PluginManager();
	~PluginManager();

	class Impl;
	std::unique_ptr<Impl> _impl;
};

} // namespace AyuPlugins
