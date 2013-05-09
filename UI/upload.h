#ifndef UPLOAD_H
#define UPLOAD_H

#include <QWidget>
#include <QProcess>

namespace Ui {
class upload;
}

class upload : public QWidget
{
    Q_OBJECT
    
public:
    QString item;
    QString user;
   QProcess *proc;

    explicit upload(QWidget *parent = 0);
    ~upload();


    
private:
    Ui::upload *ui;

public slots:
    void itemupload();

    void next();
    void completed();

signals:
    void movenext();

};

#endif // UPLOAD_H
